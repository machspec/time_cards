"""Entry point for program."""

import time_trav
import tkinter as tk


def main():
    app = time_trav.App()

    # define GUI elements

    # fields that tell the program how many parts there are and how many per bucket
    card_quantity_entries = time_trav.LabeledWidgetGroup(app, **time_trav.BOX_STYLE)
    card_quantity_entries.add_similar_widgets(time_trav.CARD_QUANTITY_FIELDS, tk.Entry)
    card_quantity_entries.build_frame()

    # fields that tell the program the details each card should display
    card_detail_entries = time_trav.LabeledWidgetGroup(app, **time_trav.BOX_STYLE)
    card_detail_entries.add_similar_widgets(time_trav.CARD_DETAIL_FIELDS, tk.Entry)
    card_detail_entries.build_frame()

    # button that sends form values to app.data
    btn_get_values = tk.Button(app, text="Get Values")
    btn_get_values.bind(
        "<Button-1>",
        lambda x: app.add_data(
            "card_data",
            time_trav.create_card_data(
                time_trav.get_group_values(card_quantity_entries),
                time_trav.get_group_values(card_detail_entries),
            ),
        ),
    )

    # draw GUI elements to the window
    card_quantity_entries.grid(sticky=tk.EW)
    card_detail_entries.grid(sticky=tk.EW)
    btn_get_values.grid(row=0, column=1)

    app.mainloop()


if __name__ == "__main__":
    main()
