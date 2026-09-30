import json

import pytest

from elements_check import ELEMENTS, analyze_bazi_chart, main


def test_known_chart_2000_01_01_noon():
    chart = analyze_bazi_chart(2000, 1, 1, 12, 0)
    assert [p.chinese for p in chart.pillars] == ["己卯", "丙子", "戊午", "戊午"]
    assert chart.day_master == "Yang Earth"
    assert chart.pillars[3].branch == "Horse"
    assert chart.pillars[3].hidden_stems == ["Yin Fire", "Yin Earth"]


def test_elements_present_counts_stems_and_branches():
    # Regression: the old script only looked at branches and reported 3 here
    chart = analyze_bazi_chart(1967, 2, 22, 19, 51)
    assert [p.chinese for p in chart.pillars] == ["丁未", "壬寅", "丁巳", "庚戌"]
    assert chart.elements_present == 5
    assert chart.missing_elements == []


def test_zodiac_is_year_animal_not_lunar_mansion():
    # Regression: getAnimal() returned the lunar-mansion animal (e.g. 乌 crow)
    assert analyze_bazi_chart(2000, 1, 1, 12).zodiac == "Rabbit"


@pytest.mark.parametrize("day, zodiac, year_pillar", [(3, "Rabbit", "癸卯"), (5, "Dragon", "甲辰")])
def test_zodiac_changes_at_li_chun(day, zodiac, year_pillar):
    # Li Chun 2024 falls on 4 February, so 3 Feb is still the Rabbit year
    chart = analyze_bazi_chart(2024, 2, day, 12)
    assert chart.zodiac == zodiac
    assert chart.pillars[0].chinese == year_pillar


def test_element_counts_totals():
    chart = analyze_bazi_chart(2000, 1, 1, 12)
    assert set(chart.element_counts) == set(ELEMENTS)
    assert sum(chart.element_counts.values()) == 8
    hidden_total = sum(len(p.hidden_stems) for p in chart.pillars)
    assert sum(chart.element_counts_hidden.values()) == 4 + hidden_total


def test_day_master_strength():
    # 戊午 day with 己, 丙, 戊 stems and Fire/Earth hidden stems: heavily supported Earth
    chart = analyze_bazi_chart(2000, 1, 1, 12)
    assert chart.day_master_strength == "Strong"
    assert 0 <= chart.day_master_support <= 1


def test_cli_json(capsys):
    main(["2000-01-01", "12:00", "--json"])
    data = json.loads(capsys.readouterr().out)
    assert data["day_master"] == "Yang Earth"
    assert data["pillars"][0]["chinese"] == "己卯"


def test_cli_rejects_bad_date():
    with pytest.raises(SystemExit):
        main(["01/01/2000"])
