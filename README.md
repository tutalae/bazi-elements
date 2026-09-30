# bazi-elements

[![tests](https://github.com/tutalae/bazi-elements/actions/workflows/tests.yml/badge.svg)](https://github.com/tutalae/bazi-elements/actions/workflows/tests.yml)

**Find out your BaZi (Chinese Four Pillars, 八字) chart and what it means, in plain English or Thai.**
You only need your birth date. Birth time and city make it more accurate. No astrology knowledge needed.

> 🇹🇭 **ภาษาไทย:** ดูดวงปาจื้อ (八字) จากวันเดือนปีเกิด พร้อมคำอธิบายภาษาไทยที่เข้าใจง่าย [อ่านวิธีใช้ภาษาไทย ↓](#ภาษาไทย-วิธีใช้งาน)

---

## Get started in 3 steps

**1. Install Python** (skip this if you already have it)
Download it from [python.org/downloads](https://www.python.org/downloads/). On Windows, tick **"Add Python to PATH"** during setup.

**2. Install bazi-elements.** Open *Terminal* (Mac) or *Command Prompt* (Windows), paste this line and press Enter:

```bash
pip install https://github.com/tutalae/bazi-elements/archive/refs/heads/main.zip
```

**3. Run it and answer the questions**

```bash
bazi-elements
```

```
Birth date (e.g. 1990-05-12 or 12/05/1990): 12/05/1990
Birth time (e.g. 14:30 or 2:30pm). Press Enter if you don't know it: 2:30pm
Birth city (e.g. Bangkok). Press Enter to skip, or type ? to see the list: Bangkok
Gender for luck periods (m/f). Press Enter to skip: f
```

That's it. You get your chart, followed by a plain-language explanation like this:

```
What your chart says
========================================

YOU  Your Day Master is Yin Fire, like a candle flame: traditionally thoughtful, caring and insightful. It is the element that stands for you.

BALANCE  Your chart is strongest in Fire and Metal, while Wood and Water only appear hidden inside the branches.
Your Day Master is Strong: it has plenty of support. Traditionally a strong chart is balanced by the elements that use its energy:
  Helpful: Earth (yellow and brown, centre); Metal (white and gold, west); Water (black and blue, north)

THEMES  The strongest influence in your chart is Companion (self, friends, siblings and independence). The quietest is Resource (learning, support, mentors and rest).

RELATIONSHIPS
  Year and Day pillars, Six Harm 六害 (丑午): small misunderstandings or hidden obstacles between family & childhood and you & your partner.
  Year and Hour pillars, Six Combination 六合 (午未): harmony and cooperation between family & childhood and children & later life.
  Day and Hour pillars, Six Clash 六冲 (丑未): tension, movement or change between you & your partner and children & later life.
  Year, Month and Hour pillars, Directional Combination 三会 (巳午未): harmony and cooperation between family & childhood, parents & career and children & later life.
  Day and Hour pillars, Bullying Punishment (partial) 恃势之刑 (丑未): friction and hard lessons between you & your partner and children & later life.

NOW
  Since 2022 you are in a 10-year Companion period (丁丑 Yin Fire Ox): a time that highlights self, friends, siblings and independence.
  This year (2026 丙午, Yang Fire Horse) is a Companion year for you: self, friends, siblings and independence.
  It harms your Day pillar (午丑), so expect small misunderstandings or hidden obstacles around you & your partner.
  It combines with your Hour pillar (午未), so expect harmony and cooperation around children & later life.

BaZi is a traditional framework for self-reflection, not a scientific prediction. Use it to think about your strengths and habits, not to make big decisions for you.
```

<details>
<summary>Show the full chart that comes before the explanation</summary>

```
Birth time: 1990-05-12 14:30 Asia/Bangkok
Solar time used: 1990-05-12 14:15
Zodiac: Horse
Day Master: Yin Fire

Pillars:
  Year  庚午  Yang Metal Horse   Direct Wealth 正财       hidden: 丁 Yin Fire (Friend), 己 Yin Earth (Eating God)
  Month 辛巳  Yin Metal  Snake   Indirect Wealth 偏财     hidden: 丙 Yang Fire (Rob Wealth), 庚 Yang Metal (Direct Wealth), 戊 Yang Earth (Hurting Officer)
  Day   丁丑  Yin Fire   Ox      Day Master               hidden: 己 Yin Earth (Eating God), 癸 Yin Water (Seven Killings), 辛 Yin Metal (Indirect Wealth)
  Hour  丁未  Yin Fire   Goat    Friend 比肩              hidden: 己 Yin Earth (Eating God), 丁 Yin Fire (Friend), 乙 Yin Wood (Indirect Resource)

Element  Surface  +Hidden     Weighted
Wood           0        1          0.1
Fire           4        5          3.6
Earth          2        4          1.6
Metal          2        4          2.4
Water          0        1          0.3

Elements present: 3/5 (missing: Wood, Water)
Day Master strength: Strong  (season: Prosperous 旺, rooted: yes, supported: no, support 39%)

Interactions:
  Six Harm 六害: 丑午 (Year, Day)
  Six Combination 六合: 午未 (Year, Hour) → Fire
  Six Clash 六冲: 丑未 (Day, Hour)
  Directional Combination 三会: 巳午未 (Year, Month, Hour) → Fire
  Bullying Punishment (partial) 恃势之刑: 丑未 (Day, Hour)

Luck pillars (starts at age 2y 2m 10d):
  age  2-11  1992  庚辰  Yang Metal Dragon  Direct Wealth 正财
  age 12-21  2002  己卯  Yin Earth  Rabbit  Eating God 食神
  age 22-31  2012  戊寅  Yang Earth Tiger   Hurting Officer 伤官
  age 32-41  2022  丁丑  Yin Fire   Ox      Friend 比肩
  age 42-51  2032  丙子  Yang Fire  Rat     Rob Wealth 劫财
  age 52-61  2042  乙亥  Yin Wood   Pig     Indirect Resource 偏印
  age 62-71  2052  甲戌  Yang Wood  Dog     Direct Resource 正印
  age 72-81  2062  癸酉  Yin Water  Rooster Seven Killings 七杀
```

</details>

**Tips**

- **Don't know your birth time?** Just press Enter. Everything except the Hour pillar still works.
- **Buddhist-era years** (พ.ศ., e.g. 12/05/2533) are converted automatically.
- **City not in the list?** Pick the nearest big city in the same country. Type `?` to see the list.
- To see it in Thai, run `bazi-elements --lang th`.

---

## Understanding your chart

A BaZi chart turns your birth moment into **four pillars**, and each pillar is a pair of Chinese characters. Here's what each part of the report means:

| Part | What it means |
|---|---|
| **Pillars** (Year, Month, Day, Hour) | Your birth year, month, day and hour, each written as two characters: a *stem* on top and a *branch* (one of the 12 animals) below. Each pillar traditionally stands for an area of life: **Year** is family and childhood, **Month** is parents and career, **Day** is you and your partner, and **Hour** is children and later life. |
| **Day Master** | The top character of your Day pillar. It represents **you**, and everything else in the chart is read in relation to it. Each Day Master is one of five elements, in a Yin or Yang form: Yang Fire is the sun, Yin Fire is a candle, and so on. |
| **Five elements** | Wood, Fire, Earth, Metal and Water. The table shows how much of each you have. *Surface* counts the visible characters, *+Hidden* adds the elements hidden inside each animal branch, and *Weighted* is the most balanced measure. |
| **Strength** | Whether your Day Master is **Strong** (well supported) or **Weak** (needs support). This decides which elements help balance you. |
| **Ten Gods** | Labels such as *Direct Wealth* or *Eating God* that describe how each part of the chart relates to you. The explanation groups them into five themes: |
| | 👥 **Companion**: self, friends, siblings · 🎨 **Output**: creativity, expression · 💰 **Wealth**: money, practical results · 🏛 **Power**: career, discipline, pressure · 📚 **Resource**: learning, support, mentors |
| **Interactions** | How pillars get along. *Combinations* suggest harmony, *clashes* suggest tension or change, and *harms* and *punishments* suggest friction. |
| **Luck pillars** | Your chart changes focus every 10 years. The explanation tells you which 10-year period you're in now and what this year brings. |

## How to use what you learn

BaZi is a **traditional tool for self-reflection**, not a scientific prediction. Some good ways to use it:

- **Know yourself.** Read your Day Master and main theme, and ask yourself: *does this match how I work and what I enjoy?*
- **Find balance.** Your *helpful elements* are traditionally linked to colours and directions. Some people use them for fun when choosing clothes, decorating a desk or planning a trip.
- **Plan the year.** The *This year* line suggests a theme to focus on, such as learning, career or relationships.
- **Understand others.** Run it for a friend or partner and compare Day Masters: a mountain (Yang Earth) and the ocean (Yang Water) work in very different ways.
- **Learn BaZi.** Compare the output with a book or a practitioner. The Chinese characters are always shown, so you can look everything up.

Don't use it to make medical, financial or other important decisions.

---

## ภาษาไทย: วิธีใช้งาน

**1. ติดตั้ง Python** จาก [python.org/downloads](https://www.python.org/downloads/) (บน Windows ให้ติ๊ก **"Add Python to PATH"**)

**2. ติดตั้งโปรแกรม:** เปิด Terminal (Mac) หรือ Command Prompt (Windows) แล้ววางคำสั่งนี้

```bash
pip install https://github.com/tutalae/bazi-elements/archive/refs/heads/main.zip
```

**3. เริ่มใช้งาน แล้วตอบคำถามทีละข้อ**

```bash
bazi-elements --lang th
```

- พิมพ์วันเกิดแบบ **วัน/เดือน/ปี** เช่น `12/05/2533` (พ.ศ. หรือ ค.ศ. ก็ได้)
- ไม่ทราบเวลาเกิด **กด Enter** ได้เลย
- พิมพ์ชื่อจังหวัดเป็นภาษาไทยได้ เช่น `กรุงเทพ`, `เชียงใหม่`, `โคราช` (พิมพ์ `?` เพื่อดูรายชื่อ)

ตัวอย่างคำอธิบาย:

```
ดวงของคุณบอกอะไร
========================================

ตัวคุณ  ธาตุประจำตัวของคุณคือ ไฟหยิน เปรียบเหมือนเปลวเทียน ตามตำราคือ ละเอียดอ่อน เอาใจใส่ และมีความคิดลึกซึ้ง ธาตุนี้เป็นตัวแทนของตัวคุณเอง

สมดุล  ดวงของคุณมีธาตุไฟและทองมากที่สุด ส่วนธาตุไม้และน้ำมีเพียงแบบแฝงอยู่ในกิ่ง
ธาตุประจำตัวของคุณแข็ง คือมีแรงหนุนมาก ตามตำรา ดวงที่แข็งจะสมดุลได้ด้วยธาตุที่ช่วยระบายพลัง:
  ธาตุที่ช่วยคุณ: ดิน (สีเหลืองและน้ำตาล ศูนย์กลาง) ทอง (สีขาวและทอง ทิศตะวันตก) น้ำ (สีดำและน้ำเงิน ทิศเหนือ)

เรื่องเด่น  อิทธิพลที่มากที่สุดในดวงคือกลุ่มเพื่อน (ตัวตน เพื่อน พี่น้อง และความเป็นอิสระ) ส่วนที่น้อยที่สุดคือกลุ่มอุปถัมภ์ (การเรียนรู้ ผู้สนับสนุน ผู้ใหญ่อุปถัมภ์ และการพักผ่อน)
```

**อ่านดวงอย่างไร:** *ธาตุประจำตัว* คือตัวคุณ *สมดุล* บอกธาตุที่มีมากและน้อย พร้อมธาตุที่ช่วยเสริม (สีและทิศ) *เรื่องเด่น* บอกเรื่องที่ดวงเน้น และ *ช่วงนี้* บอกวัยจร 10 ปีปัจจุบันและธีมของปีนี้

ปาจื้อเป็นศาสตร์สำหรับทำความเข้าใจตนเอง ไม่ใช่การทำนายทางวิทยาศาสตร์ ไม่ควรใช้แทนการตัดสินใจเรื่องสำคัญ

---

## All options

Instead of answering questions, you can put everything on one line:

```bash
bazi-elements 12/05/1990 14:30 --city Bangkok --gender female --explain
```

| Option | What it does |
|---|---|
| `--explain` | Add the plain-language explanation. It's always on in question mode. |
| `--city Bangkok` | Birth city. It sets the time zone and longitude for you. `--list-cities` shows them all, including Thai names. |
| `--gender male\|female` | Show the 10-year luck periods. |
| `--lang th` | Thai report. |
| `--tz Asia/Bangkok` `--longitude 100.5` | Set the time zone and longitude yourself, for places not in the city list. |
| `--zi-hour 23` | For births between 23:00 and 00:00: some schools start the new day at 23:00. |
| `--json` | Machine-readable output, for developers. |

## For developers

```python
from bazi_elements import analyze_bazi_chart, format_chart
from bazi_elements.explain import explain_chart

chart = analyze_bazi_chart(1990, 5, 12, 14, 30, tz="Asia/Bangkok", longitude=100.5, gender="female")
print(chart.day_master, chart.strength.verdict, chart.element_scores)
print(format_chart(chart, lang="th"))
print(explain_chart(chart, lang="en"))
```

### How it's calculated

Calendar conversion uses [lunar_python](https://github.com/6tail/lunar-python). The rest is this project.

- **Solar terms** (which set the year and month pillars) are calculated in China Standard Time. With a city or `--tz`, the birth moment is converted to that time first. For example, Li Chun 2024 was at 16:27 in China, which is 15:27 in Bangkok, so a 15:40 Bangkok birth falls in the Dragon year.
- **True solar time** for the day and hour pillars is the longitude correction (4 minutes per degree) plus the equation of time, which is accurate to about a minute.
- **Weighted element scores:** each stem counts 1. Each branch counts 1 in total, split between its hidden stems as 100%, 70/30 or 60/30/10.
- **Day Master strength** is *Strong* when at least two of these hold:
  - it is in season (旺 or 相 in the month branch),
  - it has a root in any hidden stem,
  - at least 50% of the weighted chart (excluding the Day Master) is its own element or its resource element.

  This does not model transformations or special structures (从格).
- **Helpful elements:**
  - A Strong chart gets Output, Wealth and Power.
  - A Weak chart gets Resource and Companion.
- **Interactions:** stem combinations (五合) and clashes, 六合, 六冲, 六害, 三合 (full and half), 三会, and punishments (刑). 寅巳申 and 丑戌未 are reported as *partial* when only two of the three branches appear.

### Tests

```bash
pip install -e ".[test]"
pytest
```

They run on Linux and Windows for Python 3.9, 3.11 and 3.13 on every push.

## License

MIT
