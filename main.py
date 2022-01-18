"""Entry point for program."""

import app
import tkinter as tk


def main():
    root = app.core.App()

    # define GUI elements

    # fields that tell the program how many parts there are and how many per bucket
    card_quantity_entries = app.helpers.LabeledWidgetGroup(
        root, **app.constants.BOX_STYLE
    )
    card_quantity_entries.add_similar_widgets(
        app.constants.CARD_QUANTITY_FIELDS, tk.Entry
    )
    card_quantity_entries.build_frame()

    # fields that tell the program the details each card should display
    card_detail_entries = app.helpers.LabeledWidgetGroup(
        root, **app.constants.BOX_STYLE
    )
    card_detail_entries.add_similar_widgets(app.constants.CARD_DETAIL_FIELDS, tk.Entry)
    card_detail_entries.build_frame()

    # button that sends form values to app.data
    btn_get_values = tk.Button(root, text="Get Values")
    btn_get_values.bind(
        "<Button-1>",
        lambda x: root.add_data(
            "card_data",
            app.core.create_card_data(
                app.helpers.get_group_values(card_quantity_entries),
                app.helpers.get_group_values(card_detail_entries),
            ),
        ),
    )

    # draw GUI elements to the window
    card_quantity_entries.grid(sticky=tk.EW)
    card_detail_entries.grid(sticky=tk.EW)
    btn_get_values.grid(row=0, column=1)

    root.mainloop()


if __name__ == "__main__":
    main()
