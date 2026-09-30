from datetime import date

import pytest

from bazi_elements import analyze_bazi_chart
from bazi_elements.cities import find_city
from bazi_elements.cli import parse_date, parse_time
from bazi_elements.explain import explain_chart, favourable_elements

TODAY = date(2026, 6, 1)   # a 丙午 Fire Horse year


@pytest.fixture
def chart():
    return analyze_bazi_chart(2000, 1, 1, 12, gender="male")


def test_explanation_sections(chart):
    text = explain_chart(chart, today=TODAY)
    assert "Your Day Master is Yang Earth, like a mountain" in text
    assert "no Metal at all" in text
    assert "Since 2018 you are in a 10-year Power period" in text
    assert "This year (2026 丙午, Yang Fire Horse) is a Resource year" in text
    assert "clashes with your Month pillar (午子)" in text
    assert "not a scientific prediction" in text


def test_explanation_thai(chart):
    text = explain_chart(chart, lang="th", today=TODAY)
    assert "ธาตุประจำตัวของคุณคือ ดินหยาง เปรียบเหมือนภูเขา" in text
    assert "ไม่มีธาตุทองเลย" in text
    assert "วัยจร 10 ปีแบบกลุ่มอำนาจ" in text


def test_favourable_elements_follow_strength(chart):
    # A strong Earth Day Master is balanced by Metal (output), Water (wealth) and Wood (power)
    assert chart.strength.verdict == "Strong"
    assert favourable_elements(chart) == ["Metal", "Water", "Wood"]


def test_explanation_without_gender_or_time():
    text = explain_chart(analyze_bazi_chart(2000, 1, 1, 12), today=TODAY, time_known=False)
    assert "Add --gender" in text
    assert "Hour pillar is only a guess" in text


@pytest.mark.parametrize("name", ["Bangkok", "bangkok", "กรุงเทพ", "chiang-mai", "โคราช"])
def test_find_city(name):
    assert find_city(name) is not None


def test_find_city_values():
    assert find_city("Chiang Mai") == ("Chiang Mai", "Asia/Bangkok", 98.98)
    assert find_city("Atlantis") is None


@pytest.mark.parametrize("text, expected, buddhist", [
    ("1990-05-12", date(1990, 5, 12), False),
    ("12/05/1990", date(1990, 5, 12), False),
    ("12.05.2533", date(1990, 5, 12), True),
    ("2533-05-12", date(1990, 5, 12), True),
])
def test_parse_date(text, expected, buddhist):
    assert parse_date(text) == (expected, buddhist)


@pytest.mark.parametrize("text, expected", [("14:30", "14:30"), ("2:30pm", "14:30"), ("7.05", "07:05"),
                                            ("12:15 AM", "00:15")])
def test_parse_time(text, expected):
    assert parse_time(text).strftime("%H:%M") == expected


def test_hidden_only_elements_are_not_called_missing():
    # 1990-05-12 14:30 Bangkok: no Wood or Water on the surface, but 乙 and 癸 are hidden in 未 and 丑
    chart = analyze_bazi_chart(1990, 5, 12, 14, 30, tz="Asia/Bangkok", longitude=100.5)
    text = explain_chart(chart, today=TODAY)
    assert "Wood and Water only appear hidden inside the branches" in text
    assert "at all" not in text
