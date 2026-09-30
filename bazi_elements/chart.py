"""BaZi chart calculation and five-element analysis."""
from dataclasses import dataclass, field
from datetime import datetime
from itertools import combinations
from typing import List, Optional

from lunar_python import Solar

from .data import (BRANCHES, CONTROLLED_BY, CONTROLS, DIRECTIONAL, ELEMENTS, HIDDEN_STEMS,
                   HIDDEN_WEIGHTS, PILLAR_NAMES, PRODUCED_BY, PRODUCES, SEASON_STATES,
                   SIX_CLASHES, SIX_COMBINATIONS, STEM_CLASHES, STEM_COMBINATIONS, STEMS,
                   TEN_GODS, THREE_HARMONIES, ZODIAC)
from .solar_time import to_china_time, true_solar_time


@dataclass
class HiddenStem:
    stem: str        # Chinese character, e.g. "丁"
    name: str        # e.g. "Yin Fire"
    element: str
    weight: float    # share of the branch's qi
    ten_god: str


@dataclass
class Pillar:
    name: str
    chinese: str
    stem: str
    branch: str
    stem_name: str
    branch_animal: str
    stem_element: str
    branch_element: str
    ten_god: Optional[str]   # None for the Day Master itself
    hidden_stems: List[HiddenStem]


@dataclass
class Interaction:
    kind: str                # e.g. "Six Clash"
    chinese: str             # e.g. "六冲"
    members: str             # e.g. "子午"
    pillars: List[str]
    element: Optional[str] = None


@dataclass
class LuckPillar:
    chinese: str
    stem_name: str
    branch_animal: str
    ten_god: str
    start_year: int
    start_age: int
    end_age: int


@dataclass
class Strength:
    verdict: str             # "Strong" or "Weak"
    season_state: str        # e.g. "Prosperous"
    season_state_chinese: str
    in_season: bool          # 得令
    rooted: bool             # 得地
    supported: bool          # 得势
    support: float           # weighted share of the chart supporting the Day Master


@dataclass
class BaziChart:
    birth_time: str
    chart_time: str                  # time used for the day and hour pillars
    pillars: List[Pillar]
    zodiac: str
    day_master: str
    day_master_element: str
    element_counts: dict             # 4 stems + 4 branches
    element_counts_hidden: dict      # 4 stems + every hidden stem
    element_scores: dict             # stems 1.0 each, branches split by hidden-stem weight
    elements_present: int
    missing_elements: List[str]
    strength: Strength
    interactions: List[Interaction]
    luck_pillars: List[LuckPillar] = field(default_factory=list)
    luck_start: Optional[dict] = None    # {"years", "months", "days"} after birth


def stem_name(stem):
    polarity, element = STEMS[stem]
    return f"{polarity} {element}"


def ten_god(day_stem, other_stem):
    """The Ten God of other_stem relative to the Day Master day_stem."""
    day_polarity, day_element = STEMS[day_stem]
    polarity, element = STEMS[other_stem]
    if element == day_element:
        relation = "same"
    elif element == PRODUCES[day_element]:
        relation = "output"
    elif element == CONTROLS[day_element]:
        relation = "wealth"
    elif element == CONTROLLED_BY[day_element]:
        relation = "officer"
    else:
        relation = "resource"
    return TEN_GODS[(relation, polarity == day_polarity)][0]


def season_state(element, month_branch):
    season = BRANCHES[month_branch][1]
    if element == season:
        return SEASON_STATES["same"]
    if element == PRODUCES[season]:
        return SEASON_STATES["produced_by_season"]
    if PRODUCES[element] == season:
        return SEASON_STATES["produces_season"]
    if CONTROLS[element] == season:
        return SEASON_STATES["controls_season"]
    return SEASON_STATES["controlled_by_season"]


def count_elements(elements):
    counts = {element: 0 for element in ELEMENTS}
    for element in elements:
        counts[element] += 1
    return counts


def find_interactions(stems, branches):
    found = []

    def add(kind, chinese, members, idxs, element=None):
        found.append(Interaction(kind, chinese, members, [PILLAR_NAMES[i] for i in idxs], element))

    for i, j in combinations(range(4), 2):
        pair_stems = {stems[i], stems[j]}
        pair_branches = {branches[i], branches[j]}
        for members, element in STEM_COMBINATIONS:
            if pair_stems == set(members):
                add("Stem Combination", "天干五合", members, (i, j), element)
        for members in STEM_CLASHES:
            if pair_stems == set(members):
                add("Stem Clash", "天干冲", members, (i, j))
        for members, element in SIX_COMBINATIONS:
            if pair_branches == set(members):
                add("Six Combination", "六合", members, (i, j), element)
        for members in SIX_CLASHES:
            if pair_branches == set(members):
                add("Six Clash", "六冲", members, (i, j))

    for groups, kind, chinese in ((THREE_HARMONIES, "Three Harmony", "三合"),
                                  (DIRECTIONAL, "Directional Combination", "三会")):
        for members, element in groups:
            idxs = [i for i, b in enumerate(branches) if b in members]
            present = {branches[i] for i in idxs}
            if present == set(members):
                add(kind, chinese, members, idxs, element)
            elif kind == "Three Harmony" and len(present) == 2 and members[1] in present:
                # Half harmony needs the middle (cardinal) branch
                add("Half Three Harmony", "半合", "".join(m for m in members if m in present), idxs, element)
    return found


def analyze_bazi_chart(year, month, day, hour, minute=0, *, tz=None, longitude=None,
                       zi_hour="midnight", gender=None):
    """Build the BaZi chart for a birth date and time.

    tz: IANA time zone of the birth place (e.g. "Asia/Bangkok"). When given, solar terms
        are timed exactly, so the year and month pillars are correct near their boundaries.
    longitude: degrees east of the birth place. Requires tz; the day and hour pillars are
        then based on true solar time instead of clock time.
    zi_hour: "midnight" (day changes at 00:00) or "23" (day changes at 23:00, early Zi hour).
    gender: "male" or "female", needed for the luck pillars.
    """
    if zi_hour not in ("midnight", "23"):
        raise ValueError("zi_hour must be 'midnight' or '23'")
    if gender not in (None, "male", "female"):
        raise ValueError("gender must be 'male' or 'female'")
    if longitude is not None and tz is None:
        raise ValueError("longitude needs tz so the clock time can be converted")

    birth = datetime(year, month, day, hour, minute)
    if tz is None:
        term_time = chart_time = birth
    else:
        from zoneinfo import ZoneInfo
        moment = birth.replace(tzinfo=ZoneInfo(tz))
        term_time = to_china_time(moment)
        chart_time = true_solar_time(moment, longitude) if longitude is not None else birth

    def eight_char(t):
        ec = Solar.fromYmdHms(t.year, t.month, t.day, t.hour, t.minute, t.second).getLunar().getEightChar()
        ec.setSect(1 if zi_hour == "23" else 2)
        return ec

    year_month = eight_char(term_time)
    day_hour = eight_char(chart_time)
    ganzhi = [year_month.getYear(), year_month.getMonth(), day_hour.getDay(), day_hour.getTime()]
    stems = [g[0] for g in ganzhi]
    branches = [g[1] for g in ganzhi]
    day_stem = stems[2]

    pillars = []
    for idx, (name, stem, branch) in enumerate(zip(PILLAR_NAMES, stems, branches)):
        hidden = HIDDEN_STEMS[branch]
        pillars.append(Pillar(
            name=name,
            chinese=stem + branch,
            stem=stem,
            branch=branch,
            stem_name=stem_name(stem),
            branch_animal=BRANCHES[branch][0],
            stem_element=STEMS[stem][1],
            branch_element=BRANCHES[branch][1],
            ten_god=None if idx == 2 else ten_god(day_stem, stem),
            hidden_stems=[HiddenStem(h, stem_name(h), STEMS[h][1], w, ten_god(day_stem, h))
                          for h, w in zip(hidden, HIDDEN_WEIGHTS[len(hidden)])],
        ))

    stem_elements = [p.stem_element for p in pillars]
    hidden_all = [h for p in pillars for h in p.hidden_stems]
    scores = {element: 0.0 for element in ELEMENTS}
    for element in stem_elements:
        scores[element] += 1
    for h in hidden_all:
        scores[h.element] += h.weight
    element_counts = count_elements(stem_elements + [p.branch_element for p in pillars])

    # Day Master strength: in season (得令), rooted (得地) and supported (得势); strong if 2 of 3
    day_element = STEMS[day_stem][1]
    helpers = (day_element, PRODUCED_BY[day_element])
    state, state_chinese = season_state(day_element, branches[1])
    support = (sum(1 for i, e in enumerate(stem_elements) if i != 2 and e in helpers)
               + sum(h.weight for h in hidden_all if h.element in helpers)) / 7
    in_season = state in ("Prosperous", "Strengthening")
    rooted = any(h.element == day_element for h in hidden_all)
    supported = support >= 0.5
    strength = Strength(
        verdict="Strong" if in_season + rooted + supported >= 2 else "Weak",
        season_state=state, season_state_chinese=state_chinese,
        in_season=in_season, rooted=rooted, supported=supported, support=round(support, 2),
    )

    chart = BaziChart(
        birth_time=birth.strftime("%Y-%m-%d %H:%M") + (f" {tz}" if tz else ""),
        chart_time=chart_time.strftime("%Y-%m-%d %H:%M"),
        pillars=pillars,
        zodiac=ZODIAC[year_month.getLunar().getYearShengXiaoExact()],
        day_master=stem_name(day_stem),
        day_master_element=day_element,
        element_counts=element_counts,
        element_counts_hidden=count_elements(stem_elements + [h.element for h in hidden_all]),
        element_scores={e: round(s, 2) for e, s in scores.items()},
        elements_present=sum(1 for c in element_counts.values() if c > 0),
        missing_elements=[e for e, c in element_counts.items() if c == 0],
        strength=strength,
        interactions=find_interactions(stems, branches),
    )

    if gender:
        yun = year_month.getYun(1 if gender == "male" else 0)
        chart.luck_start = {"years": yun.getStartYear(), "months": yun.getStartMonth(), "days": yun.getStartDay()}
        for da_yun in yun.getDaYun()[1:9]:  # the first entry is the period before luck starts
            gz = da_yun.getGanZhi()
            chart.luck_pillars.append(LuckPillar(
                chinese=gz, stem_name=stem_name(gz[0]), branch_animal=BRANCHES[gz[1]][0],
                ten_god=ten_god(day_stem, gz[0]), start_year=da_yun.getStartYear(),
                # lunar_python counts nominal Chinese age (虚岁); report Western age instead
                start_age=da_yun.getStartYear() - year, end_age=da_yun.getStartYear() - year + 9,
            ))
    return chart
