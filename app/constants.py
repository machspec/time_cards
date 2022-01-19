from enum import Enum, auto
from tkinter import SUNKEN


# visual style applied to widget groups
BOX_STYLE: dict = {
    "bd": 1,
    "relief": SUNKEN,
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

    FINISH: auto()
