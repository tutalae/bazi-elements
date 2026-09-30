# bazi-elements

[![tests](https://github.com/tutalae/bazi-elements/actions/workflows/tests.yml/badge.svg)](https://github.com/tutalae/bazi-elements/actions/workflows/tests.yml)

A Python library and command-line tool for **BaZi (Four Pillars of Destiny, 八字)** charts. It calculates the four pillars from a date and time of birth and analyses them: five elements, hidden stems, Ten Gods, Day Master strength, stem and branch interactions, and luck pillars. Reports are available in **English** and **Thai**.

Calendar conversion uses [lunar_python](https://github.com/6tail/lunar-python). The analysis, true-solar-time handling, translation and reporting are this project.

## Features

- **Four Pillars** in Chinese, English and Thai, e.g. `戊午` → Yang Earth Horse / ดินหยาง มะเมีย
- **Ten Gods (十神)** for every stem and hidden stem, relative to the Day Master
- **Five elements** three ways: surface count, including hidden stems (藏干), and weighted by main / middle / residual qi
- **Day Master strength** from season (得令), roots (得地) and support (得势)
- **Interactions**: stem combinations and clashes, Six Combinations (六合), Six Clashes (六冲), Three Harmony (三合, full and half) and Directional Combinations (三会)
- **Luck pillars (大运)** with starting age and year
- **Accurate time handling**: birth-place time zone for exact solar-term boundaries, optional **true solar time** from longitude, and a choice of when the day changes (midnight or 23:00)
- Text report or `--json`

## Install

```bash
pip install git+https://github.com/tutalae/bazi-elements.git
```

## Usage

```bash
bazi-elements 2000-01-01 12:00 --gender male
```

```
Birth time: 2000-01-01 12:00
Zodiac: Rabbit
Day Master: Yang Earth

Pillars:
  Year  己卯  Yin Earth  Rabbit  Rob Wealth 劫财          hidden: 乙 Yin Wood (Direct Officer)
  Month 丙子  Yang Fire  Rat     Indirect Resource 偏印   hidden: 癸 Yin Water (Direct Wealth)
  Day   戊午  Yang Earth Horse   Day Master               hidden: 丁 Yin Fire (Direct Resource), 己 Yin Earth (Rob Wealth)
  Hour  戊午  Yang Earth Horse   Friend 比肩              hidden: 丁 Yin Fire (Direct Resource), 己 Yin Earth (Rob Wealth)

Element  Surface  +Hidden     Weighted
Wood           1        1          1.0
Fire           3        3          2.4
Earth          3        5          3.6
Metal          0        0          0.0
Water          1        1          1.0

Elements present: 4/5 (missing: Metal)
Day Master strength: Strong  (season: Trapped 囚, rooted: yes, supported: yes, support 71%)

Interactions:
  Six Clash 六冲: 子午 (Month, Day)
  Six Clash 六冲: 子午 (Month, Hour)

Luck pillars (starts at age 8y 2m 10d):
  age  8-17  2008  乙亥  Yin Wood   Pig     Direct Officer 正官
  age 18-27  2018  甲戌  Yang Wood  Dog     Seven Killings 七杀
  age 28-37  2028  癸酉  Yin Water  Rooster Direct Wealth 正财
  ...
```

### Options

| Option | Description |
|---|---|
| `--tz Asia/Bangkok` | Time zone of the birth place. Solar terms (and so the year and month pillars) are then timed exactly. Without it, the time is treated as China Standard Time, which is what lunar_python assumes. |
| `--longitude 100.5` | Birth place longitude in degrees east. Uses **true solar time** for the day and hour pillars. Needs `--tz`. |
| `--zi-hour 23` | Change the day pillar at 23:00 (early Zi hour) instead of midnight. |
| `--gender male\|female` | Show luck pillars. |
| `--lang th` | Thai report. |
| `--json` | Machine-readable output. |

Thai output (`--lang th`):

```
เวลาเกิด: 2000-01-01 12:00
นักษัตร: เถาะ
ธาตุประจำตัว: ดินหยาง

เสาทั้งสี่:
  ปี     己卯  ดินหยิน      เถาะ     ชิงทรัพย์ 劫财              ธาตุแฝง: 乙 ไม้หยิน (ขุนนาง)
  เดือน  丙子  ไฟหยาง      ชวด     อุปถัมภ์รอง 偏印            ธาตุแฝง: 癸 น้ำหยิน (ทรัพย์หลัก)
  วัน    戊午  ดินหยาง      มะเมีย   ธาตุประจำตัว                 ธาตุแฝง: 丁 ไฟหยิน (อุปถัมภ์หลัก), 己 ดินหยิน (ชิงทรัพย์)
  ยาม    戊午  ดินหยาง      มะเมีย   เพื่อน 比肩                ธาตุแฝง: 丁 ไฟหยิน (อุปถัมภ์หลัก), 己 ดินหยิน (ชิงทรัพย์)
```

### From Python

```python
from bazi_elements import analyze_bazi_chart, format_chart

chart = analyze_bazi_chart(2000, 1, 1, 12, 0, tz="Asia/Bangkok", longitude=100.5, gender="female")
print(chart.day_master, chart.strength.verdict, chart.element_scores)
print(format_chart(chart, lang="th"))
```

## How it's calculated

- **Solar terms** are calculated in China Standard Time by lunar_python. With `--tz`, the birth moment is converted to that time first. For example, Li Chun 2024 was at 16:27 in China, which is 15:27 in Bangkok, so a 15:40 Bangkok birth falls in the Dragon year.
- **True solar time** is the longitude correction (4 minutes per degree) plus the equation of time, which is accurate to about a minute.
- **Weighted element scores**: each stem counts 1. Each branch counts 1 in total, split between its hidden stems as 100%, 70/30 or 60/30/10.
- **Day Master strength** is *Strong* when at least two of these hold:
  - it is in season (旺 or 相 in the month branch),
  - it has a root in any hidden stem,
  - at least 50% of the weighted chart (excluding the Day Master) is the same element or its resource element.

  This is a common rule of thumb. It does not model transformations or special structures (从格), so treat it as a guide, not a reading.
- Punishments (刑) and harms (害) are not detected yet.

## Development

```bash
pip install -e ".[test]"
pytest
```

The tests check a known chart, Ten Gods against lunar_python on 300 random dates, the Li Chun boundary with and without time zones, true solar time, the Zi-hour option, seasonal states, interactions, luck-pillar direction by gender, and the CLI. They run on Linux and Windows for Python 3.9, 3.11 and 3.13 on every push.

## License

MIT
