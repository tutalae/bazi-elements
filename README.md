# BaZi Chart Element Check

A Python command-line tool that builds a **BaZi (Four Pillars of Destiny)** chart from a date and time of birth, translates it from Chinese to English, and analyses its **five elements** (Wood, Fire, Earth, Metal, Water).

Chart calculation is done with [lunar_python](https://github.com/6tail/lunar-python). This project adds the translation, the element analysis and a simple CLI.

## Features

- Four Pillars (year, month, day, hour) in Chinese and English, e.g. `戊午` → Yang Earth Horse
- Zodiac animal, with the year changing at **Li Chun** (start of spring), as it does in BaZi
- Five-element counts, both **on the surface** (4 stems + 4 branches) and **with hidden stems** (藏干)
- Missing elements, and the **Day Master** with a simplified strength estimate
- Human-readable output or `--json`

## Usage

```bash
pip install -r requirements.txt
python elements_check.py 2000-01-01 12:00
```

```
Zodiac: Rabbit
Day Master: Yang Earth

Pillars:
  Year  己卯  Yin Earth  Rabbit   hidden: Yin Wood
  Month 丙子  Yang Fire  Rat      hidden: Yin Water
  Day   戊午  Yang Earth Horse    hidden: Yin Fire, Yin Earth
  Hour  戊午  Yang Earth Horse    hidden: Yin Fire, Yin Earth

Element  Surface  With hidden stems
Wood           1                  1
Fire           3                  3
Earth          3                  5
Metal          0                  0
Water          1                  1

Elements present: 4/5 (missing: Metal)
Day Master strength: Strong (78% support)
```

Add `--json` for machine-readable output. The time defaults to 12:00 if left out.

Use it from Python:

```python
from elements_check import analyze_bazi_chart

chart = analyze_bazi_chart(2000, 1, 1, 12, 0)
print(chart.day_master, chart.element_counts_hidden)
```

## How it's calculated

- **Time:** the local clock time you enter is used as-is, with no true-solar-time correction. The day pillar changes at midnight (lunar_python's default).
- **Hidden stems** are counted once each, without the traditional main/middle/residual weighting.
- **Day Master strength** is a simplified heuristic: the share of the other three stems and all hidden stems that are the Day Master's own element or the element that produces it. At 50% or above it's reported as *Strong*. It ignores seasonal strength, combinations and clashes, so treat it as a rough guide, not a reading.

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

The tests check a known chart (2000-01-01 12:00 → 己卯 丙子 戊午 戊午), the Li Chun zodiac boundary, and element counting.
