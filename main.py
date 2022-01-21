"""Entry point for program."""

import app
import tkinter as tk


ENTRY_STYLE: dict = {
    "bg": app.constants.BACKGROUND_COLOR_ENTRY,
    "fg": app.constants.FOREGROUND_COLOR,
}
LABEL_STYLE: dict = {
    "bg": app.constants.BACKGROUND_COLOR,
    "fg": app.constants.FOREGROUND_COLOR,
}


def main():
    root = app.core.App("Time Card Generator", (554, 265))
    root.configure(bg=app.constants.BACKGROUND_COLOR)

    # define GUI elements

    # fields that tell the program how many parts there are and how many per bucket
    card_quantity_entries = app.helpers.LabeledWidgetGroup(
        root, **app.constants.BOX_STYLE
    )
    card_quantity_entries.add_similar_widgets(
        app.constants.CARD_QUANTITY_FIELDS, tk.Entry, **ENTRY_STYLE
    )
    card_quantity_entries.build_frame(**LABEL_STYLE)

    # fields that tell the program the details each card should display
    card_detail_entries = app.helpers.LabeledWidgetGroup(
        root, **app.constants.BOX_STYLE
    )
    card_detail_entries.add_similar_widgets(
        app.constants.CARD_DETAIL_FIELDS,
        tk.Entry,
        bg=app.constants.BACKGROUND_COLOR_ENTRY,
        fg=app.constants.FOREGROUND_COLOR,
    )
    card_detail_entries.build_frame(**LABEL_STYLE)

    # entry for operations
    frame_op_entry = tk.Frame(root, bg=app.constants.BACKGROUND_COLOR)
    lbl_ops_instructions = tk.Label(
        frame_op_entry, text="Enter operations separated by commas.", **LABEL_STYLE
    )
    entry_ops = tk.Text(frame_op_entry, width=40, height=11, **ENTRY_STYLE)
    lbl_ops_instructions.grid()
    entry_ops.grid()

    # button that sends form values to app.data
    btn_get_values = tk.Button(root, text="Export Cards")
    btn_get_values.bind(
        "<Button-1>",
        lambda x: root.add_data(
            "card_data",
            app.core.create_card_data(
                app.helpers.get_group_values(card_quantity_entries),
                app.helpers.get_group_values(card_detail_entries),
                entry_ops.get("1.0", tk.END),
            ),
        ),
    )

    # draw GUI elements to the window
    card_quantity_entries.grid(sticky=tk.EW)
    card_detail_entries.grid(sticky=tk.EW)
    btn_get_values.grid(row=0, column=1)
    frame_op_entry.grid(row=1, column=1)

    root.mainloop()


if __name__ == "__main__":
    main()
