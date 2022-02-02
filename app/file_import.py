"""Classes and functions for importing data."""

from app.constants import FORM_TRANSLATIONS, BAQ_TRANSLATIONS
from app.helpers import LabeledWidgetGroup, translate_dict_key, translate_dict_keys
from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet

import pathlib
import tkinter as tk


class FormValues:
    """Container for GUI form values."""

    def __init__(
        self,
        assembly: str,
        bkt_hrs: str,
        job_num: str,
        part_name: str,
        part_num: str,
        part_qty: str,
        ops: list[str],
        **kwargs,
    ):
        self.assembly = assembly
        self.bkt_hrs = bkt_hrs
        self.job_num = job_num
        self.part_name = part_name
        self.part_num = part_num
        self.part_qty = part_qty
        self.ops = ops

    def fill_forms(self, widget_group: LabeledWidgetGroup) -> None:
        """Fill tk.Entry type widgets."""

        def set_entry_value(form: str, value: str):
            """Clear then set the value of (form) to (value)."""
            form.delete(0, tk.END)
            form.insert(0, value)

        for label, widget in widget_group.widgets.items():
            actual_key = self.__dict__.get(
                translate_dict_key(label, (BAQ_TRANSLATIONS, FORM_TRANSLATIONS))
            )

            if actual_key is None:
                continue

            set_entry_value(widget, actual_key)

    def fill_text_entry(self, widget: tk.Text) -> None:
        """Fill tk.Text type widgets."""
        widget.delete(1.0, tk.END)
        widget.insert(tk.END, ",".join(self.ops))


def form_values_from_excel(ws: Worksheet) -> FormValues:
    """Get values from an Excel sheet and output them as a FormValues object."""

    def cell_values(data: list) -> list[str]:
        """Get cell values from row or column."""
        return [i.value for i in data]

    columns = list(ws.columns)
    rows = list(ws.rows)

    headers = cell_values(rows.pop(0))
    first_row = cell_values(rows[0])

    values = translate_dict_keys(
        {k: v for k, v in zip(headers, first_row)},
        (BAQ_TRANSLATIONS,),
    )

    bkt_hrs = sum(cell_values(columns[headers.index("TotalEstHours")][1:]))
    ops = cell_values(columns[headers.index("Dept Desc")][1:])

    return FormValues(
        **values,
        bkt_hrs=bkt_hrs,
        ops=ops,
    )


def load_excel(file_path: pathlib.Path) -> Worksheet:
    wb = load_workbook(filename=file_path.absolute())
    return wb.active
