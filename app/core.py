"""Program-specific classes and functions."""

from __future__ import annotations

from dataclasses import dataclass
from app import constants
from typing import Any

import tkinter as tk
from PIL import Image, ImageFont, ImageDraw


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
    # cope
    image: Image

    bkt_hrs: str
    bkt_qty: str
    exp_vel: str
    job_num: str
    job_qty: str
    part_name: str

    ops: list[constants.Operation]

    def build_image(self):
        """Place the text values on the image."""

        def appendText(img, text, x, y):
            draw = ImageDraw.Draw(img)
            draw.text((x, y), text, constants.FONT_COLOR, constants.FONT)

            def setMaOps(img, ops):
                x = 5
                y = 92
                for index, item in enumerate(ops):
                    appendText(img, item, x, y)
                    if index in {5, 11, 17}:
                        x += 117  # whatever
                        y = 92
                    else:
                        y += 21  # :(

                    if index == 23:
                        return

            card = Image.open("resources/card.png")
            export = card.copy()

            x = 64
            y = 7
            appendText(export, self.job_num, x, y)
            y = 30
            appendText(export, self.part_num, x, y)
            y = 50
            appendText(export, self.bkt_qty, x, y)

            x = 272
            y = 7
            appendText(export, self.pro_date, x, y)

            x = 250
            y = 30
            appendText(export, self.part_name, x, y)

            x = 255
            y = 50
            appendText(export, self.job_qty, x, y)

            x = 370
            y = 50
            appendText(export, self.bkt_hrs, x, y)

            x = 410
            y = 7
            appendText(export, self.exp_vel, x, y)

            # setMaOps(export, ("wasdf" * 6))

            self.image = export
            self.get_image()

    def get_image(self):
        """Return the Card image."""
        self.image.show()


@dataclass
class CardData:
    """Contains information for a group of similar cards."""

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
        return f"{self.job_qty // self.bkt_qty + self.remainder_parts > 0}"

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


def create_card_data(
    quantities: dict[str, str], details: dict[str, str], ops: str
) -> CardData:
    """Create a new CardData object from form values."""
    qtys: dict = translate_dict_keys(quantities)
    dtls: dict = translate_dict_keys(details)
    ops: list = [i.strip().upper() for i in ops.split(",")]

    return CardData(**qtys, **dtls, ops=ops)


# TODO: Owen
def create_cards(card_data: CardData) -> list[Card]:
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
    cardList = []
    for i in range(0, card_data.part_qty, card_data.bkt_qty):
        cardList.append(
            Card(
                card_num=i % card_data.bkt_qty,
                card_count=card_data.card_count(),
                bkt_hrs=card_data.bkt_hrs,
                bkt_qty=card_data.bkt_qty,
                exp_vel=card_data.exp_vel,
                job_num=card_data.job_num,
                job_qty=card_data.job_qty,
                part_name=card_data.part_name,
            )
        )
    print(cardList)
    return cardList


def get_form_translation(label: str) -> str:
    """Get variable name from constants.FORM_TRANSLATIONS constant, given label text."""
    return constants.FORM_TRANSLATIONS[label]


def translate_dict_keys(d: dict[str, str]) -> dict:
    """Return a dict with translated keys per constants.FORM_TRANSLATIONS constant."""
    return {get_form_translation(lbl): v for lbl, v in d.items()}
