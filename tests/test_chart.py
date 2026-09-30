import random
from datetime import datetime, timedelta

import pytest
from lunar_python import Solar
from lunar_python.util import LunarUtil

from bazi_elements import analyze_bazi_chart
from bazi_elements.chart import find_interactions, season_state, ten_god
from bazi_elements.data import HIDDEN_STEMS, TEN_GODS
from bazi_elements.solar_time import true_solar_time


def ganzhi(chart):
    return [p.chinese for p in chart.pillars]


def test_known_chart_2000_01_01_noon():
    chart = analyze_bazi_chart(2000, 1, 1, 12, 0)
    assert ganzhi(chart) == ["己卯", "丙子", "戊午", "戊午"]
    assert chart.day_master == "Yang Earth"
    assert [h.name for h in chart.pillars[3].hidden_stems] == ["Yin Fire", "Yin Earth"]


def test_elements_present_counts_stems_and_branches():
    # Regression: the original script only looked at branches and reported 3 here
    chart = analyze_bazi_chart(1967, 2, 22, 19, 51)
    assert ganzhi(chart) == ["丁未", "壬寅", "丁巳", "庚戌"]
    assert chart.elements_present == 5


def test_zodiac_is_year_animal_not_lunar_mansion():
    # Regression: getAnimal() returned the lunar-mansion animal (e.g. 乌 crow)
    assert analyze_bazi_chart(2000, 1, 1, 12).zodiac == "Rabbit"


def test_hidden_stem_table_matches_lunar_python():
    assert HIDDEN_STEMS == LunarUtil.ZHI_HIDE_GAN


def test_element_totals():
    chart = analyze_bazi_chart(2000, 1, 1, 12)
    assert sum(chart.element_counts.values()) == 8
    assert sum(chart.element_scores.values()) == pytest.approx(8)
    assert sum(chart.element_counts_hidden.values()) == 4 + sum(len(p.hidden_stems) for p in chart.pillars)


# --- Ten Gods ---------------------------------------------------------------

CHINESE_TO_EN = {zh: en for en, zh in TEN_GODS.values()}


def test_ten_gods_match_lunar_python():
    random.seed(7)
    for _ in range(300):
        d = datetime(1940, 1, 1) + timedelta(minutes=random.randrange(60 * 24 * 365 * 80))
        ec = Solar.fromYmdHms(d.year, d.month, d.day, d.hour, d.minute, 0).getLunar().getEightChar()
        chart = analyze_bazi_chart(d.year, d.month, d.day, d.hour, d.minute)
        expected = [ec.getYearShiShenGan(), ec.getMonthShiShenGan(), ec.getTimeShiShenGan()]
        assert [chart.pillars[i].ten_god for i in (0, 1, 3)] == [CHINESE_TO_EN[x] for x in expected]
        expected_hidden = [ec.getYearShiShenZhi(), ec.getMonthShiShenZhi(),
                           ec.getDayShiShenZhi(), ec.getTimeShiShenZhi()]
        for pillar, gods in zip(chart.pillars, expected_hidden):
            assert [h.ten_god for h in pillar.hidden_stems] == [CHINESE_TO_EN[x] for x in gods]


def test_ten_god_examples():
    assert ten_god("甲", "甲") == "Friend"
    assert ten_god("甲", "庚") == "Seven Killings"
    assert ten_god("甲", "辛") == "Direct Officer"
    assert ten_god("甲", "癸") == "Direct Resource"
    assert analyze_bazi_chart(2000, 1, 1, 12).pillars[2].ten_god is None


# --- Time handling -----------------------------------------------------------

@pytest.mark.parametrize("day, zodiac, year_pillar", [(3, "Rabbit", "癸卯"), (5, "Dragon", "甲辰")])
def test_zodiac_changes_at_li_chun(day, zodiac, year_pillar):
    chart = analyze_bazi_chart(2024, 2, day, 12)
    assert chart.zodiac == zodiac
    assert ganzhi(chart)[0] == year_pillar


@pytest.mark.parametrize("minute, zodiac", [(20, "Rabbit"), (40, "Dragon")])
def test_li_chun_uses_birth_time_zone(minute, zodiac):
    # Li Chun 2024 was at 16:27 China time, i.e. 15:27 in Bangkok
    assert analyze_bazi_chart(2024, 2, 4, 15, minute, tz="Asia/Bangkok").zodiac == zodiac


def test_without_time_zone_clock_time_is_treated_as_china_time():
    assert analyze_bazi_chart(2024, 2, 4, 15, 40).zodiac == "Rabbit"


def test_true_solar_time_bangkok():
    from zoneinfo import ZoneInfo
    solar = true_solar_time(datetime(1990, 5, 12, 14, 30, tzinfo=ZoneInfo("Asia/Bangkok")), 100.5)
    assert solar.strftime("%H:%M") == "14:15"  # -18 min longitude, +3.6 min equation of time


def test_solar_time_can_change_hour_pillar():
    # 13:05 clock time in Bangkok is still before 13:00 solar time: Horse hour, not Goat
    clock = analyze_bazi_chart(2000, 1, 1, 13, 5, tz="Asia/Bangkok")
    solar = analyze_bazi_chart(2000, 1, 1, 13, 5, tz="Asia/Bangkok", longitude=100.5)
    assert clock.pillars[3].branch == "未"
    assert solar.pillars[3].branch == "午"


def test_longitude_requires_tz():
    with pytest.raises(ValueError):
        analyze_bazi_chart(2000, 1, 1, 12, longitude=100.5)


def test_zi_hour_option():
    assert ganzhi(analyze_bazi_chart(2000, 1, 1, 23, 30))[2] == "戊午"
    assert ganzhi(analyze_bazi_chart(2000, 1, 1, 23, 30, zi_hour="23"))[2] == "己未"


# --- Strength ----------------------------------------------------------------

@pytest.mark.parametrize("element, state", [
    ("Wood", "Prosperous"), ("Fire", "Strengthening"), ("Water", "Resting"),
    ("Metal", "Trapped"), ("Earth", "Dead"),
])
def test_season_states_in_tiger_month(element, state):
    assert season_state(element, "寅")[0] == state


def test_day_master_strength():
    s = analyze_bazi_chart(2000, 1, 1, 12).strength
    # Earth in a Water month is Trapped, but rooted in 午 and 71% supported
    assert (s.season_state, s.in_season, s.rooted, s.supported) == ("Trapped", False, True, True)
    assert s.support == pytest.approx(0.71)
    assert s.verdict == "Strong"


# --- Interactions ------------------------------------------------------------

def kinds(stems, branches):
    return {(i.kind, i.members) for i in find_interactions(list(stems), list(branches))}


def test_branch_interactions():
    found = kinds("甲乙丙丁", "申子辰午")
    assert ("Three Harmony", "申子辰") in found
    assert ("Six Clash", "子午") in found


def test_half_harmony_needs_middle_branch():
    assert ("Half Three Harmony", "申子") in kinds("甲乙丙丁", "申子寅卯")
    assert not any(k == "Half Three Harmony" for k, _ in kinds("甲乙丙丁", "申辰寅卯"))


def test_stem_and_six_combinations():
    found = kinds("甲己丙壬", "子丑寅卯")
    assert ("Stem Combination", "甲己") in found
    assert ("Stem Clash", "丙壬") in found
    assert ("Six Combination", "子丑") in found


def test_directional_combination():
    assert ("Directional Combination", "寅卯辰") in kinds("甲乙丙丁", "寅卯辰午")


# --- Luck pillars ------------------------------------------------------------

def test_luck_pillars_direction_by_gender():
    # Yin year stem 己: male runs backward from 丙子, female forward
    male = analyze_bazi_chart(2000, 1, 1, 12, gender="male").luck_pillars
    female = analyze_bazi_chart(2000, 1, 1, 12, gender="female").luck_pillars
    assert [p.chinese for p in male[:2]] == ["乙亥", "甲戌"]
    assert [p.chinese for p in female[:2]] == ["丁丑", "戊寅"]
    assert len(male) == 8
    assert male[0].start_year == 2008 and male[0].start_age == 8


def test_no_luck_pillars_without_gender():
    assert analyze_bazi_chart(2000, 1, 1, 12).luck_pillars == []


# --- Punishments and harms ---------------------------------------------------

def test_six_harm():
    assert ("Six Harm", "子未") in kinds("甲乙丙丁", "子未寅卯")


def test_full_and_partial_three_punishments():
    assert ("Ungrateful Punishment", "寅巳申") in kinds("甲乙丙丁", "寅巳申子")
    assert ("Bullying Punishment (partial)", "丑戌") in kinds("甲乙丙丁", "丑戌子卯")
    # a full punishment is not also reported as partial
    assert not any("partial" in k for k, _ in kinds("甲乙丙丁", "寅巳申子"))


def test_uncivil_and_self_punishment():
    found = kinds("甲乙丙丁", "子卯午午")
    assert ("Uncivil Punishment", "子卯") in found
    assert ("Self Punishment", "午午") in found


def test_no_self_punishment_for_other_branches():
    assert not any(k == "Self Punishment" for k, _ in kinds("甲乙丙丁", "子子寅卯"))
