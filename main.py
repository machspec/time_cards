"""Entry point for program."""

import app
import tkinter as tk


def main():
    root = app.core.App("Time Card Generator", (554, 265))
    root.configure(bg=app.constants.BACKGROUND_COLOR)
    root.iconbitmap("./time_cards.ico")

    # define GUI elements

    # fields that tell the program how many parts there are and how many per bucket
    card_quantity_entries = app.helpers.LabeledWidgetGroup(
        root, **app.constants.BOX_STYLE
    )
    card_quantity_entries.add_similar_widgets(
        app.constants.CARD_QUANTITY_FIELDS, tk.Entry, **app.constants.ENTRY_STYLE
    )
    card_quantity_entries.build_frame(**app.constants.LABEL_STYLE)

    # fields that tell the program the details each card should display
    card_detail_entries = app.helpers.LabeledWidgetGroup(
        root, **app.constants.BOX_STYLE
    )
    card_detail_entries.add_similar_widgets(
        app.constants.CARD_DETAIL_FIELDS, tk.Entry, **app.constants.ENTRY_STYLE
    )
    card_detail_entries.build_frame(**app.constants.LABEL_STYLE)

    # entry for operations
    frame_op_entry = tk.Frame(root, bg=app.constants.BACKGROUND_COLOR)
    lbl_ops_instructions = tk.Label(
        frame_op_entry,
        text="Enter operations separated by commas.",
        **app.constants.LABEL_STYLE
    )
    entry_ops = tk.Text(
        frame_op_entry, width=40, height=11, **app.constants.ENTRY_STYLE
    )
    lbl_ops_instructions.grid()
    entry_ops.grid()

    # frame for output buttons
    btn_frame = tk.Frame(root, bg=app.constants.BACKGROUND_COLOR)

    # button to create printable cards
    btn_export_cards = tk.Button(btn_frame, text="Export Cards")
    btn_export_cards.bind(
        "<Button-1>",
        lambda x: app.core.export_cards(
            app.helpers.get_group_values(card_quantity_entries),
            app.helpers.get_group_values(card_detail_entries),
            entry_ops.get("1.0", tk.END),
        ),
    )

    btn_import_data = tk.Button(btn_frame, text="Import Data")
    btn_import_data.bind(
        "<Button-1>", lambda x: app.core.import_data(card_detail_entries, entry_ops)
    )

    btn_import_data.grid(column=0, row=0)
    btn_export_cards.grid(column=1, row=0)

    # draw GUI elements to the window
    card_quantity_entries.grid(sticky=tk.EW)
    card_detail_entries.grid(sticky=tk.EW)
    btn_frame.grid(row=0, column=1)
    frame_op_entry.grid(row=1, column=1)

    root.mainloop()


if __name__ == "__main__":
    main()
