"""Entry point for program."""

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


class CardData:
    """Base class that holds program output."""

    bkt_hrs: int
    bkt_qty: int
    exp_vel: str
    job_num: str
    job_qty: int
    part_name: str
    part_num: str
    pro_date: str
    ops: list[str] = None

    # @property
    # def card_num(self) -> str:
    #     return f"{self.job_qty // self.bkt_qty}"

    # @property
    # def remaining_jobs(self) -> str:
    #     return f"{self.job_qty % self.bkt_qty}"

    def set_ops(self, data: list) -> None:
        self.ops = data

    def get_ops(self) -> list:
        return self.ops


def create_card_data(quantities: dict[str, str], details: dict[str, str]) -> CardData:
    """Create a new CardData object from form values."""
    return CardData(**quantities, **details)


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
        lambda x: create_card_data(
            time_trav.get_group_values(card_quantity_entries),
            time_trav.get_group_values(card_detail_entries),
        ),
    )

    card_quantity_entries.grid(sticky=tk.EW)
    card_detail_entries.grid(sticky=tk.EW)
    btn_get_values.grid(row=0, column=1)

    app.mainloop()


if __name__ == "__main__":
    main()
