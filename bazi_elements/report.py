"""Plain-text report of a BaziChart."""
from .data import ELEMENTS
from .i18n import LABELS, TEN_GOD_CHINESE, stem_label, translate


def width(text):
    # Thai combining marks take no column; Chinese characters take two
    return sum(0 if ("ั" <= ch <= "ฺ" or "็" <= ch <= "๎")
               else 2 if "一" <= ch <= "鿿" else 1 for ch in text)


def pad(text, size):
    return text + " " * max(0, size - width(text))


def rpad(text, size):
    return " " * max(0, size - width(text)) + text


def format_chart(chart, lang="en"):
    L = LABELS[lang]
    t = lambda term: translate(term, lang)

    def god(name):
        return f"{t(name)} {TEN_GOD_CHINESE[name]}" if name else L["day_master"]

    lines = [f"{L['birth']}: {chart.birth_time}"]
    if chart.chart_time != chart.birth_time[:16]:
        lines.append(f"{L['chart_time']}: {chart.chart_time}")
    lines += [f"{L['zodiac']}: {t(chart.zodiac)}",
              f"{L['day_master']}: {stem_label(chart.day_master, lang)}", "", f"{L['pillars']}:"]

    for p in chart.pillars:
        hidden = ", ".join(f"{h.stem} {stem_label(h.name, lang)} ({t(h.ten_god)})" for h in p.hidden_stems)
        lines.append(f"  {pad(t(p.name), 6)}{p.chinese}  {pad(stem_label(p.stem_name, lang), 11)}"
                     f"{pad(t(p.branch_animal), 8)}{pad(god(p.ten_god), 25)}{L['hidden']}: {hidden}")

    lines += ["", pad(L["element"], 8) + rpad(L["surface"], 8) + rpad(L["with_hidden"], 9) + rpad(L["weighted"], 13)]
    for e in ELEMENTS:
        lines.append(f"{pad(t(e), 8)}{chart.element_counts[e]:>8}{chart.element_counts_hidden[e]:>9}"
                     f"{chart.element_scores[e]:>13.1f}")

    missing = ", ".join(t(e) for e in chart.missing_elements) or L["none"]
    s = chart.strength
    yn = lambda flag: L["yes"] if flag else L["no"]
    lines += ["", f"{L['present']}: {chart.elements_present}/5 ({L['missing']}: {missing})",
              f"{L['strength']}: {t(s.verdict)}  ({L['season']}: {t(s.season_state)} {s.season_state_chinese}, "
              f"{L['rooted']}: {yn(s.rooted)}, {L['supported']}: {yn(s.supported)}, "
              f"{L['support']} {s.support:.0%})"]

    if chart.interactions:
        lines += ["", f"{L['interactions']}:"]
        for i in chart.interactions:
            element = f" → {t(i.element)}" if i.element else ""
            lines.append(f"  {t(i.kind)} {i.chinese}: {i.members} ({', '.join(t(n) for n in i.pillars)}){element}")

    if chart.luck_pillars:
        y, m, d = (chart.luck_start[k] for k in ("years", "months", "days"))
        start = f"{y} ปี {m} เดือน {d} วัน" if lang == "th" else f"{y}y {m}m {d}d"
        lines += ["", f"{L['luck']} ({L['luck_start']} {start}):"]
        for lp in chart.luck_pillars:
            lines.append(f"  {L['age']} {lp.start_age:>2}-{lp.end_age:<3} {lp.start_year}  {lp.chinese}  "
                         f"{pad(stem_label(lp.stem_name, lang), 11)}{pad(t(lp.branch_animal), 8)}{god(lp.ten_god)}")
    return "\n".join(lines)
