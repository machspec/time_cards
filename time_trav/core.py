"""Main Application Window"""

from __future__ import annotations

import tkinter as tk

from typing import Optional


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Time Traveler")
        self.geometry("480x240")

    def build_layout(self, layout: Layout):
        layout.pack()


class CardData:
    bkt_hrs: str
    bkt_qty: str
    exp_vel: str
    job_num: str
    job_qty: str
    part_name: str
    part_num: str
    pro_date: str
    ops: list[str] = None

    def set_ops(self, data: list) -> None:
        self.ops = data

    def get_ops(self) -> list:
        return self.ops


class Layout(tk.Frame):
    """Base layout class."""

    def __init__(self, root: tk.Tk):
        super().__init__(master=root)

        self.widgets: dict[str, tk.Widget] = dict()

    def build_layout(self):
        for index, (label, widget) in enumerate(self.widgets.items()):

            tk.Label(self, text=f"{label}:").grid(row=index, column=0, sticky=tk.E)
            widget.grid(row=index, column=1)

    def add_widgets(self, widgets: dict[str, tk.Widget]):
        for label, widget in widgets.items():
            self.widgets[label] = widget(self)

    def add_similar_widgets(self, labels: list, widget_class: object, **params):
        for label in labels:
            self.widgets[label] = widget_class(self, **params)
