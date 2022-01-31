"""Classes and functions for importing data."""

from app.helpers import LabeledWidgetGroup
from dataclasses import dataclass
from openpyxl import load_workbook

import pathlib
import tkinter as tk


@dataclass
class FormValues:
    """Container for GUI form values."""

    assembly: str
    bkt_hrs: str
    job_num: str
    part_name: str
    part_num: str
    ops: list[str]

    def fill_forms(self, widget_group: LabeledWidgetGroup) -> None:
        """Fill tk.Entry type widgets."""

        def set_entry_value(form_name: str, value: str):
            """Clear then set the value of (form) to (value)."""
            widget_group.widgets[form_name].delete(0, tk.END)
            widget_group.widgets[form_name].insert(0, value)

        set_entry_value("Assembly", self.assembly)
        set_entry_value("BktHrs", self.bkt_hrs)
        set_entry_value("Job", self.job_num)
        set_entry_value("Name", self.part_name)
        set_entry_value("Part#", self.part_num)

    def fill_text_entry(self, widget: tk.Text) -> None:
        """Fill tk.Text type widgets."""
        widget.delete(1.0, tk.END)
        widget.insert(tk.END, ",".join(self.ops))


def form_values_from_excel(file_path: pathlib.Path) -> FormValues:
    """Get values from an Excel sheet and output them as a FormValues object."""
    wb = load_workbook(filename=file_path.absolute())
    ws = wb.active

    bkt_hrs = sum([i.value for i in ws["l"]][1:])

    return FormValues(
        assembly=ws["b2"].value,
        bkt_hrs=str(bkt_hrs),
        job_num=ws["a2"].value,
        part_name=ws["g2"].value[: ws["g2"].value.find(",")]
        if "," in ws["g2"].value
        else ws["g2"].value,
        part_num=ws["f2"].value,
        ops=[i.value for i in ws["e"][1:]],
    )
