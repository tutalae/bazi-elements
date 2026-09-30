"""English and Thai labels for the text report."""

LABELS = {
    "en": {
        "birth": "Birth time", "chart_time": "Solar time used", "zodiac": "Zodiac",
        "day_master": "Day Master", "pillars": "Pillars", "hidden": "hidden",
        "element": "Element", "surface": "Surface", "with_hidden": "+Hidden", "weighted": "Weighted",
        "present": "Elements present", "missing": "missing", "none": "none",
        "strength": "Day Master strength", "season": "season", "rooted": "rooted",
        "supported": "supported", "support": "support", "yes": "yes", "no": "no",
        "interactions": "Interactions", "luck": "Luck pillars", "luck_start": "starts at age",
        "age": "age",
    },
    "th": {
        "birth": "เวลาเกิด", "chart_time": "เวลาสุริยคติจริง", "zodiac": "นักษัตร",
        "day_master": "ธาตุประจำตัว", "pillars": "เสาทั้งสี่", "hidden": "ธาตุแฝง",
        "element": "ธาตุ", "surface": "ปรากฏ", "with_hidden": "+แฝง", "weighted": "ถ่วงน้ำหนัก",
        "present": "ธาตุที่มี", "missing": "ขาด", "none": "ไม่มี",
        "strength": "กำลังธาตุประจำตัว", "season": "ฤดูกาล", "rooted": "มีราก",
        "supported": "มีแรงหนุน", "support": "แรงหนุน", "yes": "ใช่", "no": "ไม่",
        "interactions": "ปฏิสัมพันธ์", "luck": "วัยจร", "luck_start": "เริ่มเมื่ออายุ",
        "age": "อายุ",
    },
}

THAI = {
    # pillars
    "Year": "ปี", "Month": "เดือน", "Day": "วัน", "Hour": "ยาม",
    # elements and polarity
    "Wood": "ไม้", "Fire": "ไฟ", "Earth": "ดิน", "Metal": "ทอง", "Water": "น้ำ",
    "Yang": "หยาง", "Yin": "หยิน",
    # animals
    "Rat": "ชวด", "Ox": "ฉลู", "Tiger": "ขาล", "Rabbit": "เถาะ", "Dragon": "มะโรง", "Snake": "มะเส็ง",
    "Horse": "มะเมีย", "Goat": "มะแม", "Monkey": "วอก", "Rooster": "ระกา", "Dog": "จอ", "Pig": "กุน",
    # Ten Gods
    "Friend": "เพื่อน", "Rob Wealth": "ชิงทรัพย์", "Eating God": "เทพอาหาร",
    "Hurting Officer": "ทำลายขุนนาง", "Indirect Wealth": "ทรัพย์รอง", "Direct Wealth": "ทรัพย์หลัก",
    "Seven Killings": "เจ็ดสังหาร", "Direct Officer": "ขุนนาง",
    "Indirect Resource": "อุปถัมภ์รอง", "Direct Resource": "อุปถัมภ์หลัก",
    # seasonal states and strength
    "Prosperous": "เฟื่องฟู", "Strengthening": "เจริญ", "Resting": "พัก", "Trapped": "ถูกขัง", "Dead": "ดับ",
    "Strong": "แข็ง", "Weak": "อ่อน",
    # interactions
    "Stem Combination": "ฮะฟ้า", "Stem Clash": "ชงฟ้า", "Six Combination": "ลักฮะ",
    "Six Clash": "ชง", "Three Harmony": "ซาฮะ", "Half Three Harmony": "ซาฮะครึ่ง",
    "Directional Combination": "รวมทิศ", "Six Harm": "ทำร้าย",
    "Ungrateful Punishment": "ลงโทษอกตัญญู", "Ungrateful Punishment (partial)": "ลงโทษอกตัญญู (บางส่วน)",
    "Bullying Punishment": "ลงโทษรังแก", "Bullying Punishment (partial)": "ลงโทษรังแก (บางส่วน)",
    "Uncivil Punishment": "ลงโทษไร้มารยาท", "Self Punishment": "ลงโทษตนเอง",
}

TEN_GOD_CHINESE = {
    "Friend": "比肩", "Rob Wealth": "劫财", "Eating God": "食神", "Hurting Officer": "伤官",
    "Indirect Wealth": "偏财", "Direct Wealth": "正财", "Seven Killings": "七杀",
    "Direct Officer": "正官", "Indirect Resource": "偏印", "Direct Resource": "正印",
}


def translate(term, lang):
    return THAI.get(term, term) if lang == "th" else term


def stem_label(stem_name, lang):
    """'Yang Wood' in English, 'ไม้หยาง' in Thai."""
    polarity, element = stem_name.split()
    return f"{THAI[element]}{THAI[polarity]}" if lang == "th" else stem_name
