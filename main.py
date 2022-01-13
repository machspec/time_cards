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

    card_quantity_entries.grid(sticky=tk.EW)
    card_detail_entries.grid(sticky=tk.EW)

    app.mainloop()


if __name__ == "__main__":
    main()
