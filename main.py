def main():
    import time_trav
    import tkinter as tk

    app = time_trav.App()

    labels = [
        "Total Parts",
        "Parts Per Bucket",
        "Job",
        "PRO Date",
        "ExpVel",
        "Part#",
        "Name",
        "BktQty",
        "JobQty",
        "BktHrs",
    ]

    layout: time_trav.Layout = time_trav.Layout(app)
    layout.add_similar_widgets(labels, tk.Entry)
    layout.build_layout()

    layout.pack()

    app.mainloop()


if __name__ == "__main__":
    main()
