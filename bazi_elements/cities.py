"""Built-in birth places so users can pass --city instead of a time zone and longitude."""

# name: (IANA time zone, longitude in degrees east, other names)
CITIES = {
    # Thailand
    "Bangkok": ("Asia/Bangkok", 100.50, ["กรุงเทพ", "กรุงเทพมหานคร", "กทม"]),
    "Chiang Mai": ("Asia/Bangkok", 98.98, ["เชียงใหม่"]),
    "Chiang Rai": ("Asia/Bangkok", 99.83, ["เชียงราย"]),
    "Phuket": ("Asia/Bangkok", 98.39, ["ภูเก็ต"]),
    "Hat Yai": ("Asia/Bangkok", 100.47, ["หาดใหญ่", "สงขลา"]),
    "Khon Kaen": ("Asia/Bangkok", 102.84, ["ขอนแก่น"]),
    "Nakhon Ratchasima": ("Asia/Bangkok", 102.10, ["นครราชสีมา", "โคราช", "Korat"]),
    "Udon Thani": ("Asia/Bangkok", 102.79, ["อุดรธานี", "อุดร"]),
    "Ubon Ratchathani": ("Asia/Bangkok", 104.85, ["อุบลราชธานี", "อุบล"]),
    "Chon Buri": ("Asia/Bangkok", 100.98, ["ชลบุรี", "Pattaya", "พัทยา"]),
    "Nakhon Si Thammarat": ("Asia/Bangkok", 99.96, ["นครศรีธรรมราช"]),
    "Phitsanulok": ("Asia/Bangkok", 100.26, ["พิษณุโลก"]),
    # Asia
    "Beijing": ("Asia/Shanghai", 116.40, ["北京", "ปักกิ่ง"]),
    "Shanghai": ("Asia/Shanghai", 121.47, ["上海", "เซี่ยงไฮ้"]),
    "Guangzhou": ("Asia/Shanghai", 113.26, ["广州", "กวางโจว"]),
    "Shantou": ("Asia/Shanghai", 116.68, ["汕头", "ซัวเถา"]),
    "Hong Kong": ("Asia/Hong_Kong", 114.17, ["香港", "ฮ่องกง"]),
    "Taipei": ("Asia/Taipei", 121.56, ["台北", "ไทเป"]),
    "Singapore": ("Asia/Singapore", 103.82, ["สิงคโปร์"]),
    "Kuala Lumpur": ("Asia/Kuala_Lumpur", 101.69, ["กัวลาลัมเปอร์"]),
    "Jakarta": ("Asia/Jakarta", 106.85, ["จาการ์ตา"]),
    "Manila": ("Asia/Manila", 120.98, ["มะนิลา"]),
    "Ho Chi Minh City": ("Asia/Ho_Chi_Minh", 106.63, ["Saigon", "โฮจิมินห์"]),
    # North Vietnam stayed on UTC+7 while the south used UTC+8 (1959-75), matching Asia/Bangkok
    "Hanoi": ("Asia/Bangkok", 105.85, ["ฮานอย"]),
    "Vientiane": ("Asia/Vientiane", 102.63, ["เวียงจันทน์"]),
    "Phnom Penh": ("Asia/Phnom_Penh", 104.92, ["พนมเปญ"]),
    "Yangon": ("Asia/Yangon", 96.16, ["ย่างกุ้ง"]),
    "Tokyo": ("Asia/Tokyo", 139.69, ["โตเกียว"]),
    "Seoul": ("Asia/Seoul", 126.98, ["โซล"]),
    "Delhi": ("Asia/Kolkata", 77.21, ["New Delhi", "เดลี"]),
    # Rest of the world
    "London": ("Europe/London", -0.13, ["ลอนดอน"]),
    "Paris": ("Europe/Paris", 2.35, ["ปารีส"]),
    "Berlin": ("Europe/Berlin", 13.40, ["เบอร์ลิน"]),
    "New York": ("America/New_York", -74.01, ["นิวยอร์ก"]),
    "Los Angeles": ("America/Los_Angeles", -118.24, ["ลอสแองเจลิส"]),
    "Toronto": ("America/Toronto", -79.38, ["โตรอนโต"]),
    "Sydney": ("Australia/Sydney", 151.21, ["ซิดนีย์"]),
    "Melbourne": ("Australia/Melbourne", 144.96, ["เมลเบิร์น"]),
}


def _key(name):
    return "".join(ch for ch in name.lower() if ch.isalnum())


_LOOKUP = {}
for _name, (_tz, _lon, _aliases) in CITIES.items():
    for _alias in [_name, *_aliases]:
        _LOOKUP[_key(_alias)] = _name


def find_city(name):
    """Return (city name, time zone, longitude) or None. Matching ignores case, spaces and dashes."""
    city = _LOOKUP.get(_key(name))
    if city is None:
        return None
    tz, longitude, _ = CITIES[city]
    return city, tz, longitude
