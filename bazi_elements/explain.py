"""Plain-language explanation of a chart, for people new to BaZi."""
from datetime import date

from lunar_python import Solar

from .chart import stem_name, ten_god
from .data import (BRANCHES, CONTROLLED_BY, CONTROLS, PRODUCED_BY, PRODUCES, SIX_CLASHES,
                   SIX_COMBINATIONS, SIX_HARMS)
from .i18n import stem_label, translate

# Day Master images and traditional traits
DAY_MASTER = {
    "甲": (("a tall tree", "upright, growing and principled"),
          ("ต้นไม้ใหญ่", "ตรงไปตรงมา มุ่งมั่นเติบโต และมีหลักการ")),
    "乙": (("flowers and vines", "flexible, gentle and adaptable"),
          ("ดอกไม้และเถาวัลย์", "ยืดหยุ่น อ่อนโยน และปรับตัวเก่ง")),
    "丙": (("the sun", "warm, generous and outgoing"),
          ("ดวงอาทิตย์", "อบอุ่น ใจกว้าง และเปิดเผย")),
    "丁": (("a candle flame", "thoughtful, caring and insightful"),
          ("เปลวเทียน", "ละเอียดอ่อน เอาใจใส่ และมีความคิดลึกซึ้ง")),
    "戊": (("a mountain", "steady, reliable and protective"),
          ("ภูเขา", "มั่นคง น่าเชื่อถือ และชอบปกป้องผู้อื่น")),
    "己": (("garden soil", "nurturing, practical and patient"),
          ("ดินในสวน", "ชอบดูแลผู้อื่น ทำอะไรจับต้องได้ และอดทน")),
    "庚": (("an axe or raw ore", "decisive, direct and strong-willed"),
          ("ขวานหรือแร่เหล็ก", "เด็ดขาด ตรงไปตรงมา และใจแข็ง")),
    "辛": (("jewellery", "refined, precise and sensitive"),
          ("อัญมณี", "ประณีต ละเอียด และอ่อนไหว")),
    "壬": (("the ocean or a great river", "free-spirited, clever and resourceful"),
          ("มหาสมุทรหรือแม่น้ำใหญ่", "รักอิสระ ฉลาด และมีไหวพริบ")),
    "癸": (("rain and dew", "intuitive, gentle and imaginative"),
          ("ฝนและน้ำค้าง", "มีสัญชาตญาณดี อ่อนโยน และช่างจินตนาการ")),
}

# Traditional colours and directions of each element
ELEMENT_HINTS = {
    "Wood": ("green, east", "สีเขียว ทิศตะวันออก"),
    "Fire": ("red, south", "สีแดง ทิศใต้"),
    "Earth": ("yellow and brown, centre", "สีเหลืองและน้ำตาล ศูนย์กลาง"),
    "Metal": ("white and gold, west", "สีขาวและทอง ทิศตะวันตก"),
    "Water": ("black and blue, north", "สีดำและน้ำเงิน ทิศเหนือ"),
}

# The area of life each pillar traditionally stands for
PILLAR_AREAS = {
    "Year": ("family & childhood", "ครอบครัวและวัยเด็ก"),
    "Month": ("parents & career", "พ่อแม่และการงาน"),
    "Day": ("you & your partner", "ตัวคุณและคู่ครอง"),
    "Hour": ("children & later life", "ลูกและวัยปลาย"),
}

# The Ten Gods grouped into five families
FAMILY_OF = {
    "Friend": "Companion", "Rob Wealth": "Companion",
    "Eating God": "Output", "Hurting Officer": "Output",
    "Indirect Wealth": "Wealth", "Direct Wealth": "Wealth",
    "Seven Killings": "Power", "Direct Officer": "Power",
    "Indirect Resource": "Resource", "Direct Resource": "Resource",
}
FAMILIES = {
    "Companion": (("Companion", "self, friends, siblings and independence"),
                  ("กลุ่มเพื่อน", "ตัวตน เพื่อน พี่น้อง และความเป็นอิสระ")),
    "Output": (("Output", "creativity, self-expression and talent"),
               ("กลุ่มผลผลิต", "ความคิดสร้างสรรค์ การแสดงออก และพรสวรรค์")),
    "Wealth": (("Wealth", "money, practical results and managing resources"),
               ("กลุ่มทรัพย์", "เงิน ผลลัพธ์ที่จับต้องได้ และการบริหารทรัพยากร")),
    "Power": (("Power", "career, discipline, responsibility and pressure"),
              ("กลุ่มอำนาจ", "การงาน วินัย ความรับผิดชอบ และแรงกดดัน")),
    "Resource": (("Resource", "learning, support, mentors and rest"),
                 ("กลุ่มอุปถัมภ์", "การเรียนรู้ ผู้สนับสนุน ผู้ใหญ่อุปถัมภ์ และการพักผ่อน")),
}

# What each kind of interaction usually means
INTERACTION_MEANING = {
    "combination": ("harmony and cooperation", "ความกลมกลืนและการร่วมมือกัน"),
    "clash": ("tension, movement or change", "ความตึงเครียด การเคลื่อนไหว หรือการเปลี่ยนแปลง"),
    "harm": ("small misunderstandings or hidden obstacles", "ความเข้าใจผิดเล็กๆ หรืออุปสรรคที่มองไม่เห็น"),
    "punishment": ("friction and hard lessons", "การเสียดทาน และบทเรียนจากประสบการณ์ที่ยาก"),
}


def interaction_group(kind):
    if "Clash" in kind:
        return "clash"
    if "Harm" in kind:
        return "harm"
    if "Punishment" in kind:
        return "punishment"
    return "combination"


TEXT = {
    "en": {
        "title": "What your chart says",
        "you": "YOU  Your Day Master is {dm}, like {image}: traditionally {traits}. It is the element that stands for you.",
        "balance": "BALANCE  Your chart is strongest in {strong}{weak_part}.",
        "weak_part": " and weakest in {weak}",
        "missing_part": ", with no {missing} at all",
        "hidden_only_part": ", while {hidden} only appear hidden inside the branches",
        "strong_dm": "Your Day Master is Strong: it has plenty of support. Traditionally a strong chart is balanced by the elements that use its energy:",
        "weak_dm": "Your Day Master is Weak: it needs support. Traditionally a weak chart is balanced by the elements that feed it:",
        "favourable": "  Helpful: {items}",
        "themes": "THEMES  The strongest influence in your chart is {top} ({top_meaning}). The quietest is {low} ({low_meaning}).",
        "relations": "RELATIONSHIPS",
        "relation": "  {pillars} pillars, {kind} ({members}): {meaning} between {areas}.",
        "relation_self": "  {pillars} pillar, {kind} ({members}): {meaning} in {areas}.",
        "pillar": "{}", "sep": ", ", "last_sep": " and ", "element_sep": " and ",
        "no_relations": "RELATIONSHIPS  No strong clashes or combinations between your pillars.",
        "now": "NOW",
        "luck": "  Since {start} you are in a 10-year {family} period ({lp}): a time that highlights {meaning}.",
        "luck_before": "  Your first 10-year luck period starts in {start}.",
        "no_luck": "  Add --gender to see your 10-year luck periods.",
        "year": "  This year ({year} {gz}, {name}) is a {family} year for you: {meaning}.",
        "year_relation": "  It {verb} your {pillar} pillar ({members}), so expect {meaning} around {area}.",
        "clashes": "clashes with", "combines": "combines with", "harms": "harms",
        "no_time": "NOTE  No birth time was given, so the Hour pillar is only a guess.",
        "footer": "BaZi is a traditional framework for self-reflection, not a scientific prediction. Use it to think about your strengths and habits, not to make big decisions for you.",
    },
    "th": {
        "title": "ดวงของคุณบอกอะไร",
        "you": "ตัวคุณ  ธาตุประจำตัวของคุณคือ {dm} เปรียบเหมือน{image} ตามตำราคือ {traits} ธาตุนี้เป็นตัวแทนของตัวคุณเอง",
        "balance": "สมดุล  ดวงของคุณมีธาตุ{strong}มากที่สุด{weak_part}",
        "weak_part": " และมีธาตุ{weak}น้อยที่สุด",
        "missing_part": " โดยไม่มีธาตุ{missing}เลย",
        "hidden_only_part": " ส่วนธาตุ{hidden}มีเพียงแบบแฝงอยู่ในกิ่ง",
        "strong_dm": "ธาตุประจำตัวของคุณแข็ง คือมีแรงหนุนมาก ตามตำรา ดวงที่แข็งจะสมดุลได้ด้วยธาตุที่ช่วยระบายพลัง:",
        "weak_dm": "ธาตุประจำตัวของคุณอ่อน คือต้องการแรงหนุน ตามตำรา ดวงที่อ่อนจะสมดุลได้ด้วยธาตุที่ช่วยเสริม:",
        "favourable": "  ธาตุที่ช่วยคุณ: {items}",
        "themes": "เรื่องเด่น  อิทธิพลที่มากที่สุดในดวงคือ{top} ({top_meaning}) ส่วนที่น้อยที่สุดคือ{low} ({low_meaning})",
        "relations": "ความสัมพันธ์ในดวง",
        "relation": "  {pillars} {kind} ({members}): {meaning} ระหว่าง{areas}",
        "relation_self": "  {pillars} {kind} ({members}): {meaning} ในเรื่อง{areas}",
        "pillar": "เสา{}", "sep": " ", "last_sep": " กับ", "element_sep": "และ",
        "no_relations": "ความสัมพันธ์ในดวง  ไม่มีการชงหรือการรวมที่เด่นระหว่างเสา",
        "now": "ช่วงนี้",
        "luck": "  ตั้งแต่ปี {start} คุณอยู่ในวัยจร 10 ปีแบบ{family} ({lp}) เป็นช่วงที่เน้นเรื่อง{meaning}",
        "luck_before": "  วัยจร 10 ปีแรกของคุณเริ่มในปี {start}",
        "no_luck": "  ใส่ --gender เพื่อดูวัยจร 10 ปีของคุณ",
        "year": "  ปีนี้ ({year} {gz} {name}) เป็นปี{family}สำหรับคุณ: {meaning}",
        "year_relation": "  ปีนี้{verb}เสา{pillar}ของคุณ ({members}) จึงอาจมี{meaning}ในเรื่อง{area}",
        "clashes": "ชงกับ", "combines": "รวมกับ", "harms": "ทำร้าย",
        "no_time": "หมายเหตุ  ไม่ได้ระบุเวลาเกิด เสายามจึงเป็นเพียงการคาดเดา",
        "footer": "ปาจื้อเป็นศาสตร์ดั้งเดิมสำหรับการทำความเข้าใจตนเอง ไม่ใช่การทำนายทางวิทยาศาสตร์ ใช้เพื่อมองจุดแข็งและนิสัยของตัวเอง ไม่ควรใช้ตัดสินใจเรื่องสำคัญแทนคุณ",
    },
}


def favourable_elements(chart):
    dm = chart.day_master_element
    if chart.strength.verdict == "Strong":
        return [PRODUCES[dm], CONTROLS[dm], CONTROLLED_BY[dm]]   # output, wealth, power
    return [PRODUCED_BY[dm], dm]                                  # resource, companion


def family_scores(chart):
    scores = {family: 0.0 for family in FAMILIES}
    for p in chart.pillars:
        if p.ten_god:
            scores[FAMILY_OF[p.ten_god]] += 1
        for h in p.hidden_stems:
            scores[FAMILY_OF[h.ten_god]] += h.weight
    # The Day Master itself belongs to the Companion family but is not counted
    return scores


def branch_relation(a, b):
    pair = {a, b}
    if any(pair == set(m) for m in SIX_CLASHES):
        return "clashes", "clash"
    if any(pair == set(m) for m, _ in SIX_COMBINATIONS):
        return "combines", "combination"
    if any(pair == set(m) for m in SIX_HARMS):
        return "harms", "harm"
    return None


def join_list(items, sep, last_sep):
    items = list(items)
    return items[0] if len(items) == 1 else sep.join(items[:-1]) + last_sep + items[-1]


def explain_chart(chart, lang="en", today=None, time_known=True):
    """Plain-language summary of a chart. today defaults to date.today()."""
    today = today or date.today()
    T = TEXT[lang]
    th = lang == "th"
    t = lambda term: translate(term, lang)
    pick = lambda pair: pair[1] if th else pair[0]
    join = lambda items: (" " if th else ", ").join(items)

    day_stem = chart.pillars[2].stem
    image, traits = pick(DAY_MASTER[day_stem])
    lines = [T["title"], "=" * 40, "",
             T["you"].format(dm=stem_label(chart.day_master, lang), image=image, traits=traits), ""]

    scores = chart.element_scores
    ranked = sorted(scores, key=scores.get, reverse=True)
    elements = lambda items: join_list((t(e) for e in items), T["sep"], T["element_sep"])
    absent = [e for e in ranked if scores[e] == 0]
    hidden_only = [e for e in chart.missing_elements if scores[e] > 0]
    weak_part = T["weak_part"].format(weak=t(ranked[-1]))
    if absent:
        weak_part = T["missing_part"].format(missing=elements(absent))
    if hidden_only:
        weak_part = (weak_part if absent else "") + T["hidden_only_part"].format(hidden=elements(hidden_only))
    lines.append(T["balance"].format(strong=elements(ranked[:2]), weak_part=weak_part))
    lines.append(T["strong_dm"] if chart.strength.verdict == "Strong" else T["weak_dm"])
    items = [f"{t(e)} ({pick(ELEMENT_HINTS[e])})" for e in favourable_elements(chart)]
    lines += [T["favourable"].format(items=join(items) if th else "; ".join(items)), ""]

    fam = family_scores(chart)
    ranked_fam = sorted(fam, key=fam.get, reverse=True)
    top, low = pick(FAMILIES[ranked_fam[0]]), pick(FAMILIES[ranked_fam[-1]])
    lines += [T["themes"].format(top=top[0], top_meaning=top[1], low=low[0], low_meaning=low[1]), ""]

    if chart.interactions:
        lines.append(T["relations"])
        for i in chart.interactions:
            names = list(dict.fromkeys(i.pillars))
            areas = [pick(PILLAR_AREAS[n]) for n in names]
            template = T["relation_self"] if len(names) == 1 else T["relation"]
            lines.append(template.format(
                pillars=join_list((T["pillar"].format(t(n)) for n in names), T["sep"], T["last_sep"]),
                members=i.members,
                kind=f"{t(i.kind)} {i.chinese}", meaning=pick(INTERACTION_MEANING[interaction_group(i.kind)]),
                areas=join_list(areas, T["sep"], T["last_sep"])))
    else:
        lines.append(T["no_relations"])
    lines += ["", T["now"]]

    if chart.luck_pillars:
        current = [lp for lp in chart.luck_pillars if lp.start_year <= today.year < lp.start_year + 10]
        if current:
            lp = current[0]
            family = pick(FAMILIES[FAMILY_OF[lp.ten_god]])
            lines.append(T["luck"].format(start=lp.start_year, family=family[0], meaning=family[1],
                                          lp=f"{lp.chinese} {stem_label(lp.stem_name, lang)} {t(lp.branch_animal)}"))
        elif today.year < chart.luck_pillars[0].start_year:
            lines.append(T["luck_before"].format(start=chart.luck_pillars[0].start_year))
    else:
        lines.append(T["no_luck"])

    # Solar.fromYmd(...).getLunar() gives the year that has started by today (it changes at Li Chun)
    year_gz = Solar.fromYmd(today.year, today.month, today.day).getLunar().getYearInGanZhiExact()
    family = pick(FAMILIES[FAMILY_OF[ten_god(day_stem, year_gz[0])]])
    year_name = f"{stem_label(stem_name(year_gz[0]), lang)} {t(BRANCHES[year_gz[1]][0])}"
    lines.append(T["year"].format(year=today.year, gz=year_gz, name=year_name, family=family[0], meaning=family[1]))
    for p in chart.pillars:
        relation = branch_relation(year_gz[1], p.branch)
        if relation:
            verb, group = relation
            lines.append(T["year_relation"].format(verb=T[verb], pillar=t(p.name), members=year_gz[1] + p.branch,
                                                   meaning=pick(INTERACTION_MEANING[group]),
                                                   area=pick(PILLAR_AREAS[p.name])))

    if not time_known:
        lines += ["", T["no_time"]]
    lines += ["", T["footer"]]
    return "\n".join(lines)
