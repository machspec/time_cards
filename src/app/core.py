"""Program-specific classes and functions."""

from dataclasses import dataclass
from enum import Enum, auto
from app.constants import FORM_TRANSLATIONS
from typing import Any

import tkinter as tk


class App(tk.Tk):
    """Main Application."""

    data: dict[int, list[Any]] = dict()

    def __init__(self):
        super().__init__()

        self.title("Time Traveler")
        self.geometry("480x265")

    def add_data(self, key: str, item: Any):
        """Add data to the program.

        Instantiates a list if self.data[key] does not exist.

        Parameters:
            key <str>: key to which data will be added
            item <Any>: item to be added to value of (key)
        """
        if not self.data.get(key) or self.data[key] is None:
            self.data[key] = []

        self.data[key].append(item)
        print(self.data)


@dataclass
class CardData:
    """Base class that holds program output."""

    bkt_hrs: str
    bkt_qty: str
    exp_vel: str
    job_num: str
    job_qty: str
    part_name: str
    part_num: str
    part_qty: str
    pro_date: str
    ops: list[str] = None

    @property
    def card_count(self) -> str:
        return f"{self.job_qty // self.bkt_qty}"

    @property
    def remainder_parts(self) -> str:
        return f"{self.job_qty % self.bkt_qty}"

    def add_ops(self, data: list) -> None:
        """Append a new operation to the existing list.

        Instantiates a list if self.ops does not exist.
        """
        if self.ops is None:
            self.ops = []

        self.ops.append(data)

    def set_ops(self, data: list) -> None:
        """Set self.ops equal to a list of operations.

        Instantiates a list if self.ops does not exist.
        """
        if self.ops is None:
            self.ops = []

        self.ops = data

    def get_ops(self) -> list:
        return self.ops


# TODO: Add operations.
class Operation(Enum):
    """Operations that can be listed on a time card."""

    FINISH: auto()


def create_card_data(quantities: dict[str, str], details: dict[str, str]) -> CardData:
    """Create a new CardData object from form values."""
    qtys: dict = translate_dict_keys(quantities)
    dtls: dict = translate_dict_keys(details)

    return CardData(**qtys, **dtls)


def get_form_translation(label: str) -> str:
    """Get variable name from FORM_TRANSLATIONS constant, given label text."""
    return FORM_TRANSLATIONS[label]


def translate_dict_keys(d: dict[str, str]) -> dict:
    """Return a dict with translated keys per FORM_TRANSLATIONS constant."""
    return {get_form_translation(lbl): v for lbl, v in d.items()}
