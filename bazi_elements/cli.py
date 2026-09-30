"""Command-line interface.

    bazi-elements                                   # guided mode: asks a few questions
    bazi-elements 1990-05-12 14:30 --city Bangkok --gender female --explain
"""
import argparse
import json
import sys
from dataclasses import asdict
from datetime import datetime

from .cities import CITIES, find_city
from .chart import analyze_bazi_chart
from .explain import explain_chart
from .report import format_chart

PROMPTS = {
    "en": {
        "date": "Birth date (e.g. 1990-05-12 or 12/05/1990): ",
        "time": "Birth time (e.g. 14:30 or 2:30pm). Press Enter if you don't know it: ",
        "city": "Birth city (e.g. Bangkok). Press Enter to skip, or type ? to see the list: ",
        "gender": "Gender for luck periods (m/f). Press Enter to skip: ",
        "bad_date": "  Please write the date like 1990-05-12 (year-month-day) or 12/05/1990 (day/month/year).",
        "bad_time": "  Please write the time like 14:30, 07:05 or 2:30pm.",
        "bad_city": "  I don't know that city. Type ? to see the list, or press Enter to skip.",
        "bad_gender": "  Please type m, f, or press Enter.",
        "buddhist": "  (Buddhist year {be} converted to {ce})",
    },
    "th": {
        "date": "วันเกิด (วัน/เดือน/ปี เช่น 12/05/2533 หรือ 12/05/1990): ",
        "time": "เวลาเกิด (24 ชั่วโมง เช่น 14:30) กด Enter หากไม่ทราบ: ",
        "city": "จังหวัด/เมืองที่เกิด (เช่น กรุงเทพ) กด Enter เพื่อข้าม หรือพิมพ์ ? เพื่อดูรายชื่อ: ",
        "gender": "เพศ สำหรับวัยจร (m=ชาย / f=หญิง) กด Enter เพื่อข้าม: ",
        "bad_date": "  กรุณาพิมพ์วันเกิดแบบ วัน/เดือน/ปี เช่น 12/05/2533 (พ.ศ.) หรือ 12/05/1990 (ค.ศ.)",
        "bad_time": "  กรุณาใช้รูปแบบ ชั่วโมง:นาที เช่น 14:30 หรือ 07:05",
        "bad_city": "  ไม่พบเมืองนี้ พิมพ์ ? เพื่อดูรายชื่อ หรือกด Enter เพื่อข้าม",
        "bad_gender": "  กรุณาพิมพ์ m, f หรือกด Enter",
        "buddhist": "  (แปลง พ.ศ. {be} เป็น ค.ศ. {ce})",
    },
}


def parse_date(text):
    """Parse YYYY-MM-DD or DD/MM/YYYY; a year above 2400 is read as a Buddhist-era year (พ.ศ.)."""
    parts = text.strip().replace("/", "-").replace(".", "-").split("-")
    if len(parts) != 3:
        raise ValueError(text)
    if len(parts[2]) == 4:          # DD-MM-YYYY, as written in Thailand and Europe
        parts.reverse()
    year, month, day = (int(part) for part in parts)
    buddhist = year > 2400
    if buddhist:
        year -= 543
    return datetime(year, month, day).date(), buddhist


def parse_time(text):
    """Parse 14:30, 14.30, 2:30pm or 2:30 PM."""
    text = text.strip().replace(".", ":").replace(" ", "").upper()
    return datetime.strptime(text, "%I:%M%p" if text.endswith(("AM", "PM")) else "%H:%M").time()


def city_list():
    return "\n".join(f"  {name} ({', '.join(aliases)})" for name, (_, _, aliases) in CITIES.items())


def ask(prompt, parse, error):
    while True:
        answer = input(prompt).strip()
        try:
            return parse(answer)
        except (ValueError, KeyError):
            print(error)


def guided(lang):
    """Ask for the birth details step by step."""
    P = PROMPTS[lang]
    birth_date, buddhist = ask(P["date"], parse_date, P["bad_date"])
    if buddhist:
        print(P["buddhist"].format(be=birth_date.year + 543, ce=birth_date.year))
    birth_time = ask(P["time"], lambda a: parse_time(a) if a else None, P["bad_time"])

    while True:
        answer = input(P["city"]).strip()
        if answer == "?":
            print(city_list())
            continue
        if not answer or find_city(answer):
            city = find_city(answer) if answer else None
            break
        print(P["bad_city"])

    gender = ask(P["gender"], lambda a: {"": None, "m": "male", "f": "female",
                                         "ชาย": "male", "หญิง": "female"}[a.lower()], P["bad_gender"])
    print()
    return birth_date, birth_time, city, gender


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="bazi-elements",
        description="BaZi (Four Pillars) chart and five-element analysis. Run with no arguments for guided mode.",
        epilog="Example: bazi-elements 1990-05-12 14:30 --city Bangkok --gender female --explain")
    parser.add_argument("date", nargs="?", help="birth date: YYYY-MM-DD or DD/MM/YYYY (Buddhist-era years like 2533 work too)")
    parser.add_argument("time", nargs="?", help="local birth time: HH:MM or 2:30pm (leave out if unknown)")
    parser.add_argument("--city", help="birth city, e.g. Bangkok or เชียงใหม่ (sets --tz and --longitude)")
    parser.add_argument("--list-cities", action="store_true", help="show the built-in cities")
    parser.add_argument("--tz", help="IANA time zone of the birth place, e.g. Asia/Bangkok")
    parser.add_argument("--longitude", type=float,
                        help="longitude of the birth place in degrees east; uses true solar time (needs --tz)")
    parser.add_argument("--zi-hour", choices=["midnight", "23"], default="midnight",
                        help="when the day pillar changes: at midnight (default) or at 23:00")
    parser.add_argument("--gender", choices=["male", "female"], help="show 10-year luck periods")
    parser.add_argument("--lang", choices=["en", "th"], default="en", help="report language")
    parser.add_argument("--explain", action="store_true", help="add a plain-language explanation")
    parser.add_argument("--json", action="store_true", help="print the chart as JSON")
    args = parser.parse_args(argv)

    if args.list_cities:
        print(city_list())
        return 0

    city = find_city(args.city) if args.city else None
    if args.city and city is None:
        parser.error(f"unknown city {args.city!r}; use --list-cities, or give --tz and --longitude")

    if args.date is None:
        # Guided mode always explains the result
        birth_date, birth_time, guided_city, gender = guided(args.lang)
        city, args.gender, args.explain = guided_city or city, gender or args.gender, True
    else:
        try:
            birth_date, buddhist = parse_date(args.date)
            birth_time = parse_time(args.time) if args.time else None
        except ValueError:
            parser.error("write the date as 1990-05-12 or 12/05/1990, and the time as 14:30 or 2:30pm")
        if buddhist:
            print(PROMPTS[args.lang]["buddhist"].format(be=birth_date.year + 543, ce=birth_date.year).strip(),
                  file=sys.stderr)

    tz, longitude = args.tz, args.longitude
    if city:
        _, tz, longitude = city
    if longitude is not None and not tz:
        parser.error("--longitude needs --tz (or use --city)")

    when = datetime.combine(birth_date, birth_time or datetime.strptime("12:00", "%H:%M").time())
    try:
        chart = analyze_bazi_chart(when.year, when.month, when.day, when.hour, when.minute,
                                   tz=tz, longitude=longitude, zi_hour=args.zi_hour, gender=args.gender)
    except Exception as exc:  # e.g. unknown time zone
        parser.error(str(exc))

    if args.json:
        print(json.dumps(asdict(chart), ensure_ascii=False, indent=2))
        return 0
    print(format_chart(chart, args.lang))
    if args.explain:
        print("\n" + explain_chart(chart, args.lang, time_known=birth_time is not None))
    return 0


if __name__ == "__main__":
    sys.exit(main())
