"""Entry point for program."""


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

    @property
    def card_num(self) -> str:
        return f"{self.job_qty // self.bkt_qty}"

    @property
    def remaining_jobs(self) -> str:
        return f"{self.job_qty % self.bkt_qty}"

    def set_ops(self, data: list) -> None:
        self.ops = data

    def get_ops(self) -> list:
        return self.ops


def create_card_data(quantities: dict[str, str]) -> CardData:
    ...


def main():
    import time_trav
    import tkinter as tk

    app = time_trav.App()

    card_quantities: tuple = (
        "Total Parts",
        "Parts Per Bucket",
    )

    card_details: tuple = (
        "Job",
        "PRO Date",
        "ExpVel",
        "Part#",
        "Name",
        "JobQty",
        "BktHrs",
    )

    card_quantity_entries = time_trav.LabeledWidgetGroup(app, bd=1, relief=tk.SUNKEN)
    card_quantity_entries.add_similar_widgets(card_quantities, tk.Entry)
    card_quantity_entries.build_frame()

    card_detail_entries = time_trav.LabeledWidgetGroup(app, bd=1, relief=tk.SUNKEN)
    card_detail_entries.add_similar_widgets(card_details, tk.Entry)
    card_detail_entries.build_frame()

    btn_get_values = tk.Button(app, text="Get Values")
    btn_get_values.bind(
        "<Button-1>", lambda x: time_trav.get_group_values(card_detail_entries)
    )

    card_quantity_entries.grid(sticky=tk.EW)
    card_detail_entries.grid(sticky=tk.EW)
    btn_get_values.grid(row=0, column=1)

    app.mainloop()


if __name__ == "__main__":
    main()
