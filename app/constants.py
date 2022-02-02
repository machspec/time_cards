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

# input fields for card quantities
CARD_QUANTITY_FIELDS: tuple = (
    "Total Parts",
    "Parts Per Bucket",
)

# input fields for card details
CARD_DETAIL_FIELDS: tuple = (
    "Job",
    "Assembly",
    "PRO Date",
    "ExpVel",
    "Part#",
    "Name",
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
    "Assembly": "assembly",
    "BktHrs": "bkt_hrs",
    "ExpVel": "exp_vel",
    "Job": "job_num",
    "Name": "part_name",
    "Part#": "part_num",
    "Parts Per Bucket": "bkt_qty",
    "PRO Date": "pro_date",
    "Total Parts": "part_qty",
}

# dict that describes how column headers are stored as variables
BAQ_TRANSLATIONS: dict = {
    "JobNum": "job_num",
    "Asm": "assembly",
    "Opr": "opr",
    "Op Dtl Desc": "op_dtl",
    "Dept Desc": "dpt",
    "Part": "part_num",
    "Part Desc": "part_name",
    "WIP": "wip",
    "TBR": "tbr",
    "Start": "start_date",
    "Due Date": "due_date",
    "EstProdHours": "est_prod_hrs",
    "EstSetHours": "est_set_hrs",
    "TotalEstHours": "total_hrs",
    "Prod Qty": "part_qty",
}

# set of required columns
REQUIRED_COLUMNS: set = {
    "JobNum",
    "Asm",
    "Dept Desc",
    "Part",
    "Part Desc",
    "TotalEstHours",
    "Prod Qty",
}

# pdf report details
SHEET_SIZE: tuple[int] = (1548, 2003)

# warning levels
LARGE_PART_QUANTITY: int = 500
