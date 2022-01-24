"""Program-specific classes and functions."""

from __future__ import annotations

from dataclasses import dataclass
from app import constants
from typing import Any

import tkinter as tk
from PIL import Image, ImageDraw


class App(tk.Tk):
    """Main Application."""

    data: dict[int, list[Any]] = dict()

    def __init__(self, title: str, size: tuple):
        super().__init__()

        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")

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


# TODO: Owen
@dataclass
class Card:
    """Contains information for a single card."""

    card_num: str
    card_count: str

    job_num: str
    part_num: str
    bkt_qty: str
    pro_date: str
    part_name: str
    job_qty: str
    bkt_hrs: str
    exp_vel: str

    image: Image = None
    ops: list[constants.Operation] = None

    def build_image(self):
        """Put the image together."""
        card = Image.open("./app/resources/card.png")
        export = card.copy()

        self.place_text(export, self.job_num, (64, 7))
        self.place_text(export, self.part_num, (64, 30))
        self.place_text(export, self.bkt_qty, (64, 50))
        self.place_text(export, self.pro_date, (272, 7))
        self.place_text(export, self.part_name, (250, 30))
        self.place_text(export, self.job_qty, (255, 50))
        self.place_text(export, self.bkt_hrs, (370, 50))
        self.place_text(export, self.exp_vel, (410, 7))

        self.place_operations_text(export, self.ops)

        self.image = export
        self.get_image()  # test

    def place_operations_text(self, img: Image, ops: list):
        """Place operation names on the image."""
        initial_x = 5
        initial_y = 92
        offset_x = 117
        offset_y = 21

        x = initial_x
        y = initial_y

        for index, item in enumerate(ops):
            self.place_text(img, item, (x, y))

            if index in {5, 11, 17}:
                x += offset_x
                y = initial_y

            else:
                y += offset_y

            if index == 23:
                return

    def place_text(self, img: Image, text: str, coords: tuple):
        """Place card text on the image."""
        if not isinstance(text, str):
            text = f"{text}"

        draw = ImageDraw.Draw(img)
        draw.text(coords, text, constants.FONT_COLOR, constants.FONT)

    def get_image(self):
        """Return the Card image."""
        self.image.show()

    def set_ops(self, ops: list):
        """Set self.ops equal to a list of operations."""
        if self.ops is None:
            self.ops = []

        self.ops.extend(ops)


@dataclass
class CardData:
    """Contains information for a group of similar cards."""

    bkt_hrs: str
    bkt_qty: int
    exp_vel: str
    job_num: str
    job_qty: int
    part_name: str
    part_num: str
    part_qty: int
    pro_date: str
    ops: list[str] = None

    def __post_init__(self):
        self.bkt_qty = int(self.bkt_qty)
        self.job_qty = int(self.job_qty)
        self.part_qty = int(self.part_qty)

    @property
    def card_count(self) -> int:
        return self.job_qty // self.bkt_qty + self.remainder_parts > 0

    @property
    def remainder_parts(self) -> int:
        return self.job_qty % self.bkt_qty

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


# TODO: Owen
def create_cards(card_data_list: CardData) -> list[Card]:
    """Takes information from a CardData object and returns a list of Cards.

    Notes:
        CardData.part_qty is Total Parts.
        CardData.bkt_qty is Parts Per Bucket.

        Essentially, you're taking the information and repeating it, but
        the card number (top right) will change for each card in the set.

        bkt_qty will only change on the last card, and that's if there are
        parts left over from all the others. For example, say there are 101
        parts in total. Each bucket contains no more than 25 parts. This means
        that you'll have six cards. Five with a bkt_qty of 25 and one with a
        bkt_qty of 1.

        CardData has a couple of functions that should help you out here.
        card_count will give you the max number of cards, and remainder will
        give you the number of parts left over.
    """
    card_list = []

    for card_data in card_data_list:
        for i in range(0, card_data.part_qty, card_data.bkt_qty):
            card = Card(
                card_num=i % card_data.bkt_qty,
                card_count=card_data.card_count,
                job_num=card_data.job_num,
                part_num=card_data.part_num,
                bkt_qty=card_data.bkt_qty,
                pro_date=card_data.pro_date,
                part_name=card_data.part_name,
                job_qty=card_data.job_qty,
                bkt_hrs=card_data.bkt_hrs,
                exp_vel=card_data.exp_vel,
            )

            card.set_ops(card_data.get_ops())

            card_list.append(card)

        print(card_list)

    for card in card_list:
        card.build_image()


def create_card_data(
    quantities: dict[str, str], details: dict[str, str], ops: str
) -> CardData:
    """Create a new CardData object from form values."""
    qtys: dict = translate_dict_keys(quantities)
    dtls: dict = translate_dict_keys(details)
    ops: list = [i.strip().upper() for i in ops.split(",")]

    return CardData(**qtys, **dtls, ops=ops)


def get_form_translation(label: str) -> str:
    """Get variable name from constants.FORM_TRANSLATIONS constant, given label text."""
    return constants.FORM_TRANSLATIONS[label]


def translate_dict_keys(d: dict[str, str]) -> dict:
    """Return a dict with translated keys per constants.FORM_TRANSLATIONS constant."""
    return {get_form_translation(lbl): v for lbl, v in d.items()}
