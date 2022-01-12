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

    card_detail_entries = time_trav.LabeledWidgetGroup(app)
    card_detail_entries.add_similar_widgets(card_details, tk.Entry)
    card_detail_entries.build_frame()

    card_detail_entries.pack()

    app.mainloop()


if __name__ == "__main__":
    main()
