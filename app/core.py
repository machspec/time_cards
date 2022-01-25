"""Program-specific classes and functions."""

from __future__ import annotations

from app import card, constants, sheet
from datetime import datetime

import pathlib
import tkinter as tk
from PIL import Image


class App(tk.Tk):
    """Main Application."""

    def __init__(self, title: str, size: tuple):
        super().__init__()

        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")


def add_cards_to_sheets(
    sheet_template: sheet.SheetTemplate, cards: list[card.Card]
) -> list[sheet.Sheet]:
    for c in cards:
        c.build_image()

    initial_x = 0
    initial_y = (sheet_template.size[1] // 3 - cards[0].front_image.size[1] // 2) // 4
    offset_x = sheet_template.size[0] // 2
    offset_y = sheet_template.size[1] // 3

    back_x = offset_x
    front_x = initial_x
    y = initial_y

    current_sheet = sheet.Sheet(sheet_template)
    sheets = []

    for index, current_card in enumerate(cards):
        if index != 0 and not index % 6:
            sheets.append(current_sheet)
            current_sheet = sheet.Sheet(sheet_template)
            back_x = offset_x
            front_x = initial_x
            y = initial_y

        current_card.build_image()

        if index == 0 or not index % 2:
            front_x = initial_x
            back_x = offset_x

            current_sheet.back.paste(current_card.back_image, (back_x, y))
            current_sheet.front.paste(current_card.front_image, (front_x, y))

        else:
            front_x += offset_x
            back_x -= offset_x

            current_sheet.back.paste(current_card.back_image, (back_x, y))
            current_sheet.front.paste(current_card.front_image, (front_x, y))

            y += offset_y

    if not current_sheet in sheets:
        sheets.append(current_sheet)

    return sheets


def create_cards(card_data: card.CardData) -> list[card.Card]:
    """Takes information from a CardData object and returns a list of Cards."""
    card_list = []

    for card_index in range(0, card_data.card_count):
        current_card = card.Card(
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

        card_list.append(current_card)
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
    sheet_template = sheet.SheetTemplate(constants.SHEET_SIZE)

    card_data: card.CardData = create_card_data(quantities, details, ops)
    card_list: list[card.Card] = create_cards(card_data)
    sheets = add_cards_to_sheets(sheet_template, card_list)
    generate_page_images(card_list[0].job_num, sheets)


def generate_page_images(output_dir_name: str, sheets: list[sheet.Sheet]):
    """Create image files from list of Sheets."""
    export_time = datetime.now().strftime("%m.%d.%Y-%H.%M")
    path = pathlib.Path(f"./output/{output_dir_name}-{export_time}")
    path.mkdir(parents=True, exist_ok=True)

    for page_num, s in enumerate(sheets):
        s.front.save(path / f"{page_num}-front.jpg")
        s.back.save(path / f"{page_num}-back.jpg")


def get_form_translation(label: str) -> str:
    """Get variable name from constants.FORM_TRANSLATIONS constant, given label text."""
    return constants.FORM_TRANSLATIONS[label]


def translate_dict_keys(d: dict[str, str]) -> dict:
    """Return a dict with translated keys per constants.FORM_TRANSLATIONS constant."""
    return {get_form_translation(lbl): v for lbl, v in d.items()}
