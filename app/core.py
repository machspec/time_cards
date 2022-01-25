"""Program-specific classes and functions."""

from __future__ import annotations

from dataclasses import dataclass
import math
from app import card, constants, sheet
from typing import Any

import tkinter as tk
from PIL import Image, ImageDraw, ImageFont


class App(tk.Tk):
    """Main Application."""

    def __init__(self, title: str, size: tuple):
        super().__init__()

        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")


def add_cards_to_sheets(sheet_template: sheet.SheetTemplate, cards: list[card.Card]):
    sheet_back = Image.new("RGB", sheet_template.size, "white")
    sheet_front = Image.new("RGB", sheet_template.size, "white")

    front_card_block = Image.new("RGB", (774 * 2, 463 * 3), "white")
    back_card_block = Image.new("RGB", (774 * 2, 463 * 3), "white")

    initial_x = 0
    initial_y = 0
    offset_x = 774
    offset_y = 463

    x = initial_x
    y = initial_y

    for i, card in enumerate(cards):
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


def create_cards(card_data_list: card.CardData) -> list[card.Card]:
    """Takes information from a CardData object and returns a list of Cards."""
    card_list = []

    for card_data in card_data_list:
        for card_index in range(0, card_data.card_count):
            card = card.Card(
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

            card_list.append(card)
            card_index += 1

    return card_list


def create_card_data(
    quantities: dict[str, str], details: dict[str, str], ops: str
) -> card.CardData:
    """Create a new card.CardData object from form values."""
    qtys: dict = translate_dict_keys(quantities)
    dtls: dict = translate_dict_keys(details)
    ops: list = [i.strip().upper() for i in ops.split(",")]

    return card.CardData(**qtys, **dtls, ops=ops)


def export_cards(quantities: dict[str, str], details: dict[str, str], ops: str):
    """Run full card-creation process."""
    sheet_template = sheet.SheetTemplate((2550, 3300))

    card_data: card.CardData = create_card_data(quantities, details, ops)
    card_list: list[card.Card] = create_cards(card_data)
    sheets = add_cards_to_sheets(sheet_template, card_list)

    sheets[0].front.show()


def get_form_translation(label: str) -> str:
    """Get variable name from constants.FORM_TRANSLATIONS constant, given label text."""
    return constants.FORM_TRANSLATIONS[label]


def translate_dict_keys(d: dict[str, str]) -> dict:
    """Return a dict with translated keys per constants.FORM_TRANSLATIONS constant."""
    return {get_form_translation(lbl): v for lbl, v in d.items()}
