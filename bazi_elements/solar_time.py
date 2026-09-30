"""Clock time to true solar time conversion."""
import math
from datetime import timedelta, timezone

# lunar_python calculates solar terms in China Standard Time
CHINA_STANDARD_TIME = timezone(timedelta(hours=8))


def equation_of_time(day_of_year):
    """Minutes that apparent solar time runs ahead of mean solar time (accurate to about a minute)."""
    b = math.radians(360 / 365 * (day_of_year - 81))
    return 9.87 * math.sin(2 * b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)


def true_solar_time(moment, longitude):
    """Local apparent solar time for a timezone-aware datetime at a longitude (degrees east)."""
    if moment.tzinfo is None:
        raise ValueError("moment must be timezone-aware")
    utc = moment.astimezone(timezone.utc).replace(tzinfo=None)
    mean_solar = utc + timedelta(minutes=longitude * 4)
    return mean_solar + timedelta(minutes=equation_of_time(mean_solar.timetuple().tm_yday))


def to_china_time(moment):
    """Wall-clock time in China Standard Time for a timezone-aware datetime."""
    return moment.astimezone(CHINA_STANDARD_TIME).replace(tzinfo=None)
