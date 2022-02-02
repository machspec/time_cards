"""Generic classes and functions."""

from __future__ import annotations

import tkinter as tk

from abc import ABC, abstractmethod


class NoTranslationError(BaseException):
    ...


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

    def __init__(self, root: tk.Tk, **frame_params):
        super().__init__(master=root, **frame_params)

        self.widgets: dict[str, tk.Widget] = dict()

    def add_similar_widgets(
        self, labels: tuple[str], widget_class: object, **widget_params
    ):
        """Add several widgets of the same type to the collection.

        parameters:
        - labels <tuple>: labels for each widget
        - widget_class <object>: type of all widgets to be added
        - widget_params: optional parameters passed to all widgets
        """

        for label in labels:
            self.widgets[label] = widget_class(self, **widget_params)

    def add_widgets(self, widgets: dict[str, tk.Widget], **widget_params):
        """Add several widgets to the collection.

        parameters:
        - widgets <dict>: dictionary {label_text: widget_type}
        - widget_params: optional parameters passed to all widgets
        """
        for label, widget in widgets.items():
            self.widgets[label] = widget(self, **widget_params)

    def build_frame(self, **lbl_params):
        """Grid-attach all widgets and labels.

        Optional keyword arguments assigned to labels.
        """

        self.grid_columnconfigure(0, weight=1)

        for index, (label, widget) in enumerate(self.widgets.items()):
            tk.Label(self, text=f"{label}:", **lbl_params).grid(
                row=index, column=0, sticky=tk.E
            )

            widget.grid(row=index, column=1, padx=5, pady=5, sticky=tk.E)


def get_form_translation(label: str, translations: dict) -> str:
    """Get variable name from a translations dict, given label text."""
    return translations[label]


def get_group_values(group: WidgetGroup) -> dict[str, str]:
    """Return dictionary of values from WidgetGroup."""
    return {label: value.get() for label, value in group.widgets.items()}


def translate_dict_key(key: str, translations: tuple[dict]) -> str:
    """Return a translated string per a group of translations."""
    for translation in translations:
        try:
            return get_form_translation(key, translation)

        except KeyError:
            continue

    raise NoTranslationError("Key does not exist within any supplied dictionaries.")


def translate_dict_keys(dictionary: dict[str, str], translations: tuple[dict]) -> dict:
    """Return a dict with translated keys per a group of translations."""
    for translation in translations:
        try:
            return {
                get_form_translation(lbl, translation): v
                for lbl, v in dictionary.items()
            }

        except KeyError:
            continue

    raise NoTranslationError("Keys do not correspond to any supplied dictionaries.")
