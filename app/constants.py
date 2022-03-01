from tkinter import SUNKEN
from PIL import ImageFont


# app information
APP_VERSION: str = "v0.3.7"
GITHUB_RELEASES_URL: str = "https://github.com/machspec/time_cards/releases"
GITHUB_API_URL: str = "https://api.github.com/repos/machspec/time_cards/releases"
GUI_SIZE: tuple = (554, 285)

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
    "Asm": "assembly",
    "HrsPerPiece": "hrs_per_piece",
    "JobNum": "job_num",
    "Op Dtl Desc": "dpt",
    "Part": "part_num",
    "Part Name": "part_name",
    "PRO Date": "pro_date",
    "ProdQty": "part_qty",
    "TotalEstHours": "total_hrs",
}

# set of required columns
REQUIRED_COLUMNS: set = {
    "Asm",
    "HrsPerPiece",
    "JobNum",
    "Op Dtl Desc",
    "Part",
    "Part Name",
    "PRO Date",
    "ProdQty",
    "TotalEstHours",
}

# pdf report details
SHEET_SIZE: tuple[int] = (1599, 2065)

# warning levels
LARGE_PART_QUANTITY: int = 500
