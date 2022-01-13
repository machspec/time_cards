"""Core classes for program."""

from __future__ import annotations

import tkinter as tk

from abc import ABC, abstractmethod


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Time Traveler")
        self.geometry("480x265")


class WidgetGroup(ABC, tk.Frame):
    """Group of related widgets."""

    @abstractmethod
    def add_similar_widgets(self, labels: tuple[str], widget_class: object):
        ...

    @abstractmethod
    def add_widgets(self, widgets: dict[str, tk.Widget]):
        ...

    @abstractmethod
    def build_frame(self):
        ...


class LabeledWidgetGroup(WidgetGroup):
    """Frame with rows consisting of a label followed by a widget."""

    def __init__(self, root: tk.Tk, **params):
        super().__init__(master=root, **params)

        self.widgets: dict[str, tk.Widget] = dict()

    def add_similar_widgets(self, labels: tuple[str], widget_class: object, **params):
        """Add several widgets of the same type to the collection.

        parameters:
            labels <tuple>: labels for each widget
            widget_class <object>: type of all widgets to be added
            params: optional parameters passed to all widgets
        """
        for label in labels:
            self.widgets[label] = widget_class(self, **params)

    def add_widgets(self, widgets: dict[str, tk.Widget], **params):
        """Add several widgets to the collection.

        parameters:
            widgets <dict>: dictionary {label_text: widget_type}
            params: optional parameters passed to all widgets
        """
        for label, widget in widgets.items():
            self.widgets[label] = widget(self, **params)

    def build_frame(self):
        """Grid-attach all widgets and labels."""

        self.grid_columnconfigure(0, weight=1)
        for index, (label, widget) in enumerate(self.widgets.items()):
            tk.Label(self, text=f"{label}:").grid(row=index, column=0, sticky=tk.E)
            widget.grid(row=index, column=1, padx=5, pady=5, sticky=tk.E)


def get_group_values(group: WidgetGroup) -> dict[str, str]:
    """Return dictionary of values from WidgetGroup."""
    return {label: value.get() for label, value in group.widgets.items()}
