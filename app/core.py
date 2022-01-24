"""Program-specific classes and functions."""

from __future__ import annotations

from dataclasses import dataclass
import math
from app import constants
from typing import Any

import tkinter as tk
from PIL import Image, ImageDraw, ImageFont


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
    ops: list[constants.Operation]

    back_image: Image = None
    front_image: Image = None

    # TODO: Jacob
    def build_back_image(self):
        """Put the image together."""
        card_back = Image.open("./app/resources/card_back.jpg")

        back_output = card_back.copy()

        # place text on back image
        self.place_text(back_output, self.job_num, (53, 6))
        self.place_text(back_output, self.pro_date, (125, 185))
        self.place_text(
            back_output,
            f"{self.card_num}/{self.card_count}",
            (720, 9),
            constants.FONT_SMALL,
        )

        self.place_text(back_output, self.part_num, (78, 43))
        self.place_text(back_output, self.part_name, (78, 76))

        self.place_text(back_output, self.bkt_qty, (357, 6))
        self.place_text(back_output, self.job_qty, (103, 150))

        self.back_image = back_output

    def build_front_image(self):
        """Put the image together."""
        card_front = Image.open("./app/resources/card_front.jpg")

        front_output = card_front.copy()

        # place text on front image
        self.place_text(front_output, self.job_num, (55, 5))
        self.place_text(front_output, self.pro_date, (448, 5))
        self.place_text(front_output, self.exp_vel, (676, 5))
        self.place_text(
            front_output,
            f"{self.card_num}/{self.card_count}",
            (720, 9),
            constants.FONT_SMALL,
        )

        self.place_text(front_output, self.part_num, (82, 42))
        self.place_text(front_output, self.part_name, (412, 42))

        self.place_text(front_output, self.bkt_qty, (92, 78))
        self.place_text(front_output, self.job_qty, (425, 78))
        self.place_text(front_output, self.bkt_hrs, (613, 78))

        self.place_operations_text(front_output, self.ops)

        self.front_image = front_output

    def build_image(self):
        self.build_front_image()
        self.build_back_image()

    def place_operations_text(self, img: Image, ops: list):
        """Place operation names on the image."""
        initial_x = 8
        initial_y = 145
        offset_x = 196
        offset_y = 34

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

    def place_text(
        self, img: Image, text: str, coords: tuple, font: ImageFont = constants.FONT
    ):
        """Place card text on the image."""
        if not isinstance(text, str):
            text = f"{text}"

        draw = ImageDraw.Draw(img)
        draw.text(coords, text, constants.FONT_COLOR, font)

    def set_ops(self, ops: list):
        """Set self.ops equal to a list of operations."""
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
        return math.ceil(self.part_qty // self.bkt_qty) + (self.remainder_parts > 0)

    @property
    def remainder_parts(self) -> int:
        return self.part_qty % self.bkt_qty

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


def create_cards(card_data_list: CardData) -> list[Card]:
    """Takes information from a CardData object and returns a list of Cards."""
    card_list = []

    for card_data in card_data_list:
        print(card_data.remainder_parts)
        for card_index in range(0, card_data.card_count):
            card = Card(
                card_num=card_index + 1,
                card_count=card_data.card_count,
                job_num=card_data.job_num,
                part_num=card_data.part_num,
                bkt_qty=int(
                    card_data.remainder_parts and card_index + 1 == card_data.card_count
                )
                or card_data.bkt_qty,
                pro_date=card_data.pro_date,
                part_name=card_data.part_name,
                job_qty=card_data.job_qty,
                bkt_hrs=card_data.bkt_hrs,
                exp_vel=card_data.exp_vel,
                ops=card_data.ops,
            )

            # card.set_ops(card_data.get_ops())

            card_list.append(card)
            card_index += 1

    front_card_block = Image.new("RGB", (774 * 2, 463 * 3), "white")
    back_card_block = Image.new("RGB", (774 * 2, 463 * 3), "white")

    initial_x = 0
    initial_y = 0
    offset_x = 774
    offset_y = 463

    x = initial_x
    y = initial_y
    for i, card in enumerate(card_list):
        card.build_image()

        if i == 0 or not i % 2:
            x = 0
            front_card_block.paste(card.front_image, (x, y))
            back_card_block.paste(card.back_image, (x, y))

        else:
            x += offset_x

            front_card_block.paste(card.front_image, (x, y))
            back_card_block.paste(card.back_image, (x, y))

            y += offset_y

    front_card_block.show()
    back_card_block.show()


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
