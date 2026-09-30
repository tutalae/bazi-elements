"""
BaZi (Four Pillars of Destiny) chart and five-element check.

Converts a Gregorian date and time into a BaZi chart with lunar_python,
translates it to English, and counts the five elements, both on the
surface (stems + branches) and including the hidden stems in each branch.

Usage:
    python elements_check.py 2000-01-01 12:00
    python elements_check.py 2000-01-01 12:00 --json
"""
import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime

from lunar_python import Solar

ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]

STEMS = {
    "甲": ("Yang", "Wood"), "乙": ("Yin", "Wood"),
    "丙": ("Yang", "Fire"), "丁": ("Yin", "Fire"),
    "戊": ("Yang", "Earth"), "己": ("Yin", "Earth"),
    "庚": ("Yang", "Metal"), "辛": ("Yin", "Metal"),
    "壬": ("Yang", "Water"), "癸": ("Yin", "Water"),
}

BRANCHES = {
    "子": ("Rat", "Water"), "丑": ("Ox", "Earth"), "寅": ("Tiger", "Wood"),
    "卯": ("Rabbit", "Wood"), "辰": ("Dragon", "Earth"), "巳": ("Snake", "Fire"),
    "午": ("Horse", "Fire"), "未": ("Goat", "Earth"), "申": ("Monkey", "Metal"),
    "酉": ("Rooster", "Metal"), "戌": ("Dog", "Earth"), "亥": ("Pig", "Water"),
}

ZODIAC = {
    "鼠": "Rat", "牛": "Ox", "虎": "Tiger", "兔": "Rabbit", "龙": "Dragon", "蛇": "Snake",
    "马": "Horse", "羊": "Goat", "猴": "Monkey", "鸡": "Rooster", "狗": "Dog", "猪": "Pig",
}

# Production cycle: each element produces the next one
PRODUCES = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal", "Metal": "Water", "Water": "Wood"}
PRODUCED_BY = {child: parent for parent, child in PRODUCES.items()}

PILLAR_NAMES = ["Year", "Month", "Day", "Hour"]


@dataclass
class Pillar:
    name: str
    chinese: str
    stem: str           # e.g. "Yang Earth"
    branch: str         # e.g. "Horse"
    stem_element: str
    branch_element: str
    hidden_stems: list  # e.g. ["Yin Fire", "Yin Earth"]


@dataclass
class BaziChart:
    pillars: list
    zodiac: str
    day_master: str
    element_counts: dict          # 4 stems + 4 branches
    element_counts_hidden: dict   # 4 stems + every hidden stem
    elements_present: int
    missing_elements: list
    day_master_support: float     # share of the chart supporting the Day Master
    day_master_strength: str


def stem_name(stem):
    polarity, element = STEMS[stem]
    return f"{polarity} {element}"


def count_elements(elements):
    counts = {element: 0 for element in ELEMENTS}
    for element in elements:
        counts[element] += 1
    return counts


def analyze_bazi_chart(year, month, day, hour, minute=0):
    """Build the BaZi chart for a local date and time."""
    lunar = Solar.fromYmdHms(year, month, day, hour, minute, 0).getLunar()
    eight_char = lunar.getEightChar()

    ganzhi = [eight_char.getYear(), eight_char.getMonth(), eight_char.getDay(), eight_char.getTime()]
    hidden = [eight_char.getYearHideGan(), eight_char.getMonthHideGan(),
              eight_char.getDayHideGan(), eight_char.getTimeHideGan()]

    pillars = []
    for name, (stem, branch), hidden_stems in zip(PILLAR_NAMES, ganzhi, hidden):
        pillars.append(Pillar(
            name=name,
            chinese=stem + branch,
            stem=stem_name(stem),
            branch=BRANCHES[branch][0],
            stem_element=STEMS[stem][1],
            branch_element=BRANCHES[branch][1],
            hidden_stems=[stem_name(h) for h in hidden_stems],
        ))

    stem_elements = [p.stem_element for p in pillars]
    element_counts = count_elements(stem_elements + [p.branch_element for p in pillars])
    hidden_elements = [STEMS[h][1] for stems in hidden for h in stems]
    element_counts_hidden = count_elements(stem_elements + hidden_elements)

    # Simplified Day Master strength: the share of the other stems and all hidden
    # stems that are the Day Master's own element or the element that produces it.
    day_element = pillars[2].stem_element
    others = stem_elements[:2] + stem_elements[3:] + hidden_elements
    supporting = sum(1 for e in others if e in (day_element, PRODUCED_BY[day_element]))
    support = supporting / len(others)

    return BaziChart(
        pillars=pillars,
        zodiac=ZODIAC[lunar.getYearShengXiaoExact()],  # year changes at Li Chun, like the BaZi year
        day_master=pillars[2].stem,
        element_counts=element_counts,
        element_counts_hidden=element_counts_hidden,
        elements_present=sum(1 for count in element_counts.values() if count > 0),
        missing_elements=[e for e, count in element_counts.items() if count == 0],
        day_master_support=round(support, 2),
        day_master_strength="Strong" if support >= 0.5 else "Weak",
    )


def format_chart(chart):
    lines = [f"Zodiac: {chart.zodiac}", f"Day Master: {chart.day_master}", "", "Pillars:"]
    for p in chart.pillars:
        lines.append(f"  {p.name:<5} {p.chinese}  {p.stem:<10} {p.branch:<8} hidden: {', '.join(p.hidden_stems)}")

    lines += ["", f"{'Element':<7}  Surface  With hidden stems"]
    for element in ELEMENTS:
        lines.append(f"{element:<7}  {chart.element_counts[element]:>7}  {chart.element_counts_hidden[element]:>17}")

    missing = ", ".join(chart.missing_elements) or "none"
    lines += ["",
              f"Elements present: {chart.elements_present}/5 (missing: {missing})",
              f"Day Master strength: {chart.day_master_strength} ({chart.day_master_support:.0%} support)"]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="BaZi chart and five-element check")
    parser.add_argument("date", help="birth date, YYYY-MM-DD")
    parser.add_argument("time", nargs="?", default="12:00", help="local birth time, HH:MM (default 12:00)")
    parser.add_argument("--json", action="store_true", help="print the chart as JSON")
    args = parser.parse_args(argv)

    try:
        when = datetime.strptime(f"{args.date} {args.time}", "%Y-%m-%d %H:%M")
    except ValueError:
        parser.error("use YYYY-MM-DD for the date and HH:MM for the time")

    chart = analyze_bazi_chart(when.year, when.month, when.day, when.hour, when.minute)
    if args.json:
        print(json.dumps(asdict(chart), ensure_ascii=False, indent=2))
    else:
        print(format_chart(chart))


if __name__ == "__main__":
    sys.exit(main())
