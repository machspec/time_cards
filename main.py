"""Entry point for program."""

from app import constants, core, helpers
import tkinter as tk


def main():
    root = core.App("Time Card Generator", (554, 265))
    root.configure(bg=constants.BACKGROUND_COLOR)
    root.iconbitmap("./time_cards.ico")
    root.resizable(False, False)

    # define GUI elements

    # fields that tell the program how many parts there are and how many per bucket
    card_quantity_entries = helpers.LabeledWidgetGroup(root, **constants.BOX_STYLE)
    card_quantity_entries.add_similar_widgets(
        constants.CARD_QUANTITY_FIELDS, tk.Entry, **constants.ENTRY_STYLE
    )
    card_quantity_entries.build_frame(**constants.LABEL_STYLE)

    # fields that tell the program the details each card should display
    card_detail_entries = helpers.LabeledWidgetGroup(root, **constants.BOX_STYLE)
    card_detail_entries.add_similar_widgets(
        constants.CARD_DETAIL_FIELDS, tk.Entry, **constants.ENTRY_STYLE
    )
    card_detail_entries.build_frame(**constants.LABEL_STYLE)

    # tk.Text entry for operations
    frame_op_entry = tk.Frame(root, bg=constants.BACKGROUND_COLOR)
    lbl_ops_instructions = tk.Label(
        frame_op_entry,
        text="Enter operations separated by commas.",
        **constants.LABEL_STYLE
    )
    text_ops = tk.Text(frame_op_entry, width=40, height=11, **constants.ENTRY_STYLE)

    # frame for IO buttons
    frame_io_buttons = tk.Frame(root, bg=constants.BACKGROUND_COLOR)

    # button to import data from a file
    btn_import_data = tk.Button(frame_io_buttons, text="Import Data")
    btn_import_data.bind(
        "<Button-1>",
        lambda _: core.import_data(
            (card_quantity_entries, card_detail_entries), text_ops
        ),
    )

    # button to create printable cards
    btn_export_cards = tk.Button(frame_io_buttons, text="Export Cards")
    btn_export_cards.bind(
        "<Button-1>",
        lambda _: core.export_cards(
            helpers.get_group_values(card_quantity_entries),
            helpers.get_group_values(card_detail_entries),
            text_ops.get("1.0", tk.END),
        ),
    )

    # draw GUI elements to the window

    # IO buttons -> frame_io_buttons
    btn_import_data.grid(column=0, row=0)
    btn_export_cards.grid(column=1, row=0)

    # operations textbox and instructions -> frame_op_entry
    lbl_ops_instructions.grid()
    text_ops.grid()

    # all widgets -> root
    card_quantity_entries.grid(sticky=tk.EW)
    card_detail_entries.grid(sticky=tk.EW)
    frame_io_buttons.grid(row=0, column=1)
    frame_op_entry.grid(row=1, column=1)

    root.mainloop()


if __name__ == "__main__":
    main()
