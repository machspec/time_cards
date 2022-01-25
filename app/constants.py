from enum import Enum, auto
from tkinter import SUNKEN
from PIL import ImageFont

# program color palette
BACKGROUND_COLOR: str = "#333333"
BACKGROUND_COLOR_ENTRY: str = "#555555"
FOREGROUND_COLOR: str = "#eeeeee"

# widget styles
BOX_STYLE: dict = {
    "bd": 1,
    "relief": SUNKEN,
    "bg": "#333333",
}

ENTRY_STYLE: dict = {
    "bg": BACKGROUND_COLOR_ENTRY,
    "fg": FOREGROUND_COLOR,
}

LABEL_STYLE: dict = {
    "bg": BACKGROUND_COLOR,
    "fg": FOREGROUND_COLOR,
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

# font for program output
FONT = ImageFont.truetype("./app/resources/RobotoMono-Regular.ttf", 22, encoding="unic")
FONT_COLOR = (0, 0, 0)
FONT_SMALL = ImageFont.truetype(
    "./app/resources/RobotoMono-Regular.ttf", 15, encoding="unic"
)

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
