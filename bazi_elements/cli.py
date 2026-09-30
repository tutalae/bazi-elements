"""Command-line interface: bazi-elements 2000-01-01 12:00"""
import argparse
import json
import sys
from dataclasses import asdict
from datetime import datetime

from .chart import analyze_bazi_chart
from .report import format_chart


def main(argv=None):
    parser = argparse.ArgumentParser(prog="bazi-elements",
                                     description="BaZi (Four Pillars) chart and five-element analysis")
    parser.add_argument("date", help="birth date, YYYY-MM-DD")
    parser.add_argument("time", nargs="?", default="12:00", help="local birth time, HH:MM (default 12:00)")
    parser.add_argument("--tz", help="IANA time zone of the birth place, e.g. Asia/Bangkok")
    parser.add_argument("--longitude", type=float,
                        help="longitude of the birth place in degrees east; uses true solar time (needs --tz)")
    parser.add_argument("--zi-hour", choices=["midnight", "23"], default="midnight",
                        help="when the day pillar changes: at midnight (default) or at 23:00")
    parser.add_argument("--gender", choices=["male", "female"], help="show luck pillars")
    parser.add_argument("--lang", choices=["en", "th"], default="en", help="report language")
    parser.add_argument("--json", action="store_true", help="print the chart as JSON")
    args = parser.parse_args(argv)

    try:
        when = datetime.strptime(f"{args.date} {args.time}", "%Y-%m-%d %H:%M")
    except ValueError:
        parser.error("use YYYY-MM-DD for the date and HH:MM for the time")
    if args.longitude is not None and not args.tz:
        parser.error("--longitude needs --tz")

    try:
        chart = analyze_bazi_chart(when.year, when.month, when.day, when.hour, when.minute,
                                   tz=args.tz, longitude=args.longitude,
                                   zi_hour=args.zi_hour, gender=args.gender)
    except Exception as exc:  # e.g. unknown time zone
        parser.error(str(exc))

    if args.json:
        print(json.dumps(asdict(chart), ensure_ascii=False, indent=2))
    else:
        print(format_chart(chart, args.lang))
    return 0


if __name__ == "__main__":
    sys.exit(main())
