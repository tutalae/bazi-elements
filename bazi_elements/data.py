"""Lookup tables for stems, branches, elements and their relationships."""

ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]

# stem: (polarity, element)
STEMS = {
    "甲": ("Yang", "Wood"), "乙": ("Yin", "Wood"),
    "丙": ("Yang", "Fire"), "丁": ("Yin", "Fire"),
    "戊": ("Yang", "Earth"), "己": ("Yin", "Earth"),
    "庚": ("Yang", "Metal"), "辛": ("Yin", "Metal"),
    "壬": ("Yang", "Water"), "癸": ("Yin", "Water"),
}

# branch: (animal, element)
BRANCHES = {
    "子": ("Rat", "Water"), "丑": ("Ox", "Earth"), "寅": ("Tiger", "Wood"),
    "卯": ("Rabbit", "Wood"), "辰": ("Dragon", "Earth"), "巳": ("Snake", "Fire"),
    "午": ("Horse", "Fire"), "未": ("Goat", "Earth"), "申": ("Monkey", "Metal"),
    "酉": ("Rooster", "Metal"), "戌": ("Dog", "Earth"), "亥": ("Pig", "Water"),
}

# Hidden stems (藏干), main qi first
HIDDEN_STEMS = {
    "子": ["癸"], "丑": ["己", "癸", "辛"], "寅": ["甲", "丙", "戊"], "卯": ["乙"],
    "辰": ["戊", "乙", "癸"], "巳": ["丙", "庚", "戊"], "午": ["丁", "己"], "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"], "酉": ["辛"], "戌": ["戊", "辛", "丁"], "亥": ["壬", "甲"],
}

# Weight of main / middle / residual qi, by number of hidden stems in the branch
HIDDEN_WEIGHTS = {1: [1.0], 2: [0.7, 0.3], 3: [0.6, 0.3, 0.1]}

ZODIAC = {
    "鼠": "Rat", "牛": "Ox", "虎": "Tiger", "兔": "Rabbit", "龙": "Dragon", "蛇": "Snake",
    "马": "Horse", "羊": "Goat", "猴": "Monkey", "鸡": "Rooster", "狗": "Dog", "猪": "Pig",
}

# Production and control cycles
PRODUCES = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal", "Metal": "Water", "Water": "Wood"}
CONTROLS = {"Wood": "Earth", "Earth": "Water", "Water": "Fire", "Fire": "Metal", "Metal": "Wood"}
PRODUCED_BY = {child: parent for parent, child in PRODUCES.items()}
CONTROLLED_BY = {target: source for source, target in CONTROLS.items()}

# Ten Gods, keyed by (relationship to the Day Master, same polarity?)
TEN_GODS = {
    ("same", True): ("Friend", "比肩"),
    ("same", False): ("Rob Wealth", "劫财"),
    ("output", True): ("Eating God", "食神"),
    ("output", False): ("Hurting Officer", "伤官"),
    ("wealth", True): ("Indirect Wealth", "偏财"),
    ("wealth", False): ("Direct Wealth", "正财"),
    ("officer", True): ("Seven Killings", "七杀"),
    ("officer", False): ("Direct Officer", "正官"),
    ("resource", True): ("Indirect Resource", "偏印"),
    ("resource", False): ("Direct Resource", "正印"),
}

# Seasonal strength (旺相休囚死) of an element relative to the month's element
SEASON_STATES = {
    "same": ("Prosperous", "旺"),
    "produced_by_season": ("Strengthening", "相"),
    "produces_season": ("Resting", "休"),
    "controls_season": ("Trapped", "囚"),
    "controlled_by_season": ("Dead", "死"),
}

# Branch interactions: (members, resulting element or None)
SIX_COMBINATIONS = [("子丑", "Earth"), ("寅亥", "Wood"), ("卯戌", "Fire"),
                    ("辰酉", "Metal"), ("巳申", "Water"), ("午未", "Fire")]
SIX_CLASHES = ["子午", "丑未", "寅申", "卯酉", "辰戌", "巳亥"]
THREE_HARMONIES = [("申子辰", "Water"), ("亥卯未", "Wood"), ("寅午戌", "Fire"), ("巳酉丑", "Metal")]
DIRECTIONAL = [("寅卯辰", "Wood"), ("巳午未", "Fire"), ("申酉戌", "Metal"), ("亥子丑", "Water")]
SIX_HARMS = ["子未", "丑午", "寅巳", "卯辰", "申亥", "酉戌"]
# Three-branch punishments: (members, English name, Chinese name)
THREE_PUNISHMENTS = [("寅巳申", "Ungrateful Punishment", "无恩之刑"),
                     ("丑戌未", "Bullying Punishment", "恃势之刑")]
UNCIVIL_PUNISHMENT = "子卯"
SELF_PUNISHMENT = "辰午酉亥"   # each punishes itself when it appears twice
STEM_COMBINATIONS = [("甲己", "Earth"), ("乙庚", "Metal"), ("丙辛", "Water"), ("丁壬", "Wood"), ("戊癸", "Fire")]
STEM_CLASHES = ["甲庚", "乙辛", "丙壬", "丁癸"]

PILLAR_NAMES = ["Year", "Month", "Day", "Hour"]
