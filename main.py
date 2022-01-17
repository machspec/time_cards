"""Entry point for program."""

from dataclasses import dataclass
from enum import Enum, auto

import time_trav
import tkinter as tk


BOX_STYLE: dict = {
    "bd": 1,
    "relief": tk.SUNKEN,
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


@dataclass
class CardData:
    """Base class that holds program output."""

    bkt_hrs: str
    bkt_qty: str
    exp_vel: str
    job_num: str
    job_qty: str
    part_name: str
    part_num: str
    part_qty: str
    pro_date: str
    ops: list[str] = None

    # @property
    # def card_num(self) -> str:
    #     return f"{self.job_qty // self.bkt_qty}"

    # @property
    # def remaining_jobs(self) -> str:
    #     return f"{self.job_qty % self.bkt_qty}"

    def add_ops(self, data: list) -> None:
        """Append a new operation to the existing list.

        Instantiates a list if self.ops does not exist.
        """
        if self.ops is None:
            self.ops = []

        self.ops.append(data)

    def set_ops(self, data: list) -> None:
        """Set self.ops equal to a list of operations.

        Instantiates a list if self.ops does not exist.
        """
        if self.ops is None:
            self.ops = []

        self.ops = data

    def get_ops(self) -> list:
        return self.ops


# TODO: Add operations.
class Operation(Enum):
    """Operations that can be listed on a time card."""

    FINISH: auto()


def create_card_data(quantities: dict[str, str], details: dict[str, str]) -> CardData:
    """Create a new CardData object from form values."""

    def get_form_translation(label: str) -> str:
        """Get variable name from FORM_TRANSLATIONS constant, given label text."""
        return FORM_TRANSLATIONS[label]

    def translate_dict_keys(d: dict[str, str]) -> dict:
        """Return a dict with translated keys per FORM_TRANSLATIONS constant."""
        return {get_form_translation(lbl): v for lbl, v in d.items()}

    qtys: dict = translate_dict_keys(quantities)
    dtls: dict = translate_dict_keys(details)

    return CardData(**qtys, **dtls)


def main():
    app = time_trav.App()

    card_quantity_entries = time_trav.LabeledWidgetGroup(app, **BOX_STYLE)
    card_quantity_entries.add_similar_widgets(CARD_QUANTITY_FIELDS, tk.Entry)
    card_quantity_entries.build_frame()

    card_detail_entries = time_trav.LabeledWidgetGroup(app, **BOX_STYLE)
    card_detail_entries.add_similar_widgets(CARD_DETAIL_FIELDS, tk.Entry)
    card_detail_entries.build_frame()

    btn_get_values = tk.Button(app, text="Get Values")
    btn_get_values.bind(
        "<Button-1>",
        lambda x: app.add_data(
            create_card_data(
                time_trav.get_group_values(card_quantity_entries),
                time_trav.get_group_values(card_detail_entries),
            )
        ),
    )

    card_quantity_entries.grid(sticky=tk.EW)
    card_detail_entries.grid(sticky=tk.EW)
    btn_get_values.grid(row=0, column=1)

    app.mainloop()


if __name__ == "__main__":
    main()
