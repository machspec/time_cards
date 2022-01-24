from enum import Enum, auto
from tkinter import SUNKEN
from PIL import ImageFont

# background color of elements
BACKGROUND_COLOR: str = "#333333"
BACKGROUND_COLOR_ENTRY: str = "#555555"

# visual style applied to widget groups
BOX_STYLE: dict = {
    "bd": 1,
    "relief": SUNKEN,
    "bg": "#333333",
}

CARD_QUANTITY_FIELDS: tuple = (
    "Total Parts",
    "Parts Per Bucket",
)

CARD_DETAIL_FIELDS: tuple = (
    "Job",
    "PRO Date",
    "ExpVel",
    "Part#",
    "Name",
    "JobQty",
    "BktHrs",
)

# only works on windows
FONT = ImageFont.truetype("./app/resources/RobotoMono-Regular.ttf", 22, encoding="unic")
FONT_COLOR = (0, 0, 0)
FONT_SMALL = ImageFont.truetype(
    "./app/resources/RobotoMono-Regular.ttf", 15, encoding="unic"
)

# foreground (text) color of elements
FOREGROUND_COLOR: str = "#eeeeee"

# dict that describes how form labels are stored as variables
FORM_TRANSLATIONS: dict = {
    "BktHrs": "bkt_hrs",
    "ExpVel": "exp_vel",
    "Job": "job_num",
    "JobQty": "job_qty",
    "Name": "part_name",
    "Part#": "part_num",
    "Parts Per Bucket": "bkt_qty",
    "PRO Date": "pro_date",
    "Total Parts": "part_qty",
}

# TODO: Add operations.
class Operation(Enum):
    """Operations that can be listed on a time card."""

    _1600 = auto()
    _5400 = auto()
    _5400_2 = auto()
    CUBLEX = auto()
    DUOBLOCK = auto()
    EDM = auto()
    FINISH = auto()
    GRIND = auto()
    HS6A = auto()
    HT1100 = auto()
    HT25 = auto()
    HU50A = auto()
    HU50B = auto()
    HU50C = auto()
    KNC32A = auto()
    KJR16 = auto()
    LATHE1 = auto()
    LATHE2 = auto()
    MAM25A = auto()
    MAM25B = auto()
    MAM25C = auto()
    MAM63C = auto()
    NLX = auto()
    NT1 = auto()
    NT2 = auto()
    NT3 = auto()
    NT4 = auto()
    NT6 = auto()
    NT7 = auto()
    NT8 = auto()
    NT9 = auto()
    NT10 = auto()
    NT11 = auto()
    NT12 = auto()
    NT13 = auto()
    NT14 = auto()
    NT15 = auto()
    NT17 = auto()
    NT18 = auto()
    NT19 = auto()
    OKUMA = auto()
    RA1 = auto()
    RA3 = auto()
    RA4 = auto()
    RA41LIVE = auto()
    ROBO = auto()
    ROBO2 = auto()
    SR32 = auto()
    SR38 = auto()
    TOOL = auto()
    TOYOTA = auto()
    VMT = auto()
    WFL = auto()
    YASDAA = auto()
    YASDAB = auto()
    YASDAC = auto()
