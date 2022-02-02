"""Program-specific classes and functions."""

from __future__ import annotations

from app import card, constants, file_import, helpers, sheet
from datetime import datetime
from PIL import Image
from tkinter import messagebox

import pathlib
import subprocess
import tkinter as tk
import tkinter.filedialog


class App(tk.Tk):
    """Main Application."""

    def __init__(self, title: str, size: tuple):
        super().__init__()

        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")


def add_cards_to_sheets(
    sheet_template: sheet.SheetTemplate, cards: list[card.Card]
) -> list[sheet.Sheet]:
    """Build card images and add them to sheets, front and back."""

    for c in cards:
        c.build_card()

    initial_x = 0
    initial_y = (sheet_template.size[1] // 3 - cards[0].front_image.size[1] // 2) // 4

    offset_x = sheet_template.size[0] // 2
    offset_y = sheet_template.size[1] // 3

    front_x = initial_x
    back_x = offset_x + 10
    y = initial_y

    current_sheet = sheet.Sheet(sheet_template)
    sheets = []

    for index, current_card in enumerate(cards):
        if index != 0 and not index % 6:
            sheets.append(current_sheet)
            current_sheet = sheet.Sheet(sheet_template)

            front_x = initial_x
            back_x = offset_x + 10
            y = initial_y

        if index == 0 or not index % 2:
            front_x = initial_x
            back_x = offset_x + 10

            current_sheet.back.paste(current_card.back_image, (back_x, y))
            current_sheet.front.paste(current_card.front_image, (front_x, y))

        else:
            front_x += offset_x
            back_x -= offset_x - 10

            current_sheet.back.paste(current_card.back_image, (back_x, y))
            current_sheet.front.paste(current_card.front_image, (front_x, y))

            y += offset_y

    if not current_sheet in sheets:
        sheets.append(current_sheet)

    return sheets


def add_uniform_margin(
    sheet_template: sheet.SheetTemplate,
    sheets: list[sheet.Sheet],
    final_page_size: tuple[int],
) -> list[sheet.Sheet]:
    """Add uniform margin to sheet images."""

    def paste_to_margin(params, s: sheet.Sheet, offset: tuple[int]) -> None:
        """Paste the sheet, front and back, onto the margin image."""
        front_margins = Image.new(*params)
        back_margins = Image.new(*params)

        front_margins.paste(s.front, offset)
        back_margins.paste(s.back, offset)

        s.front = front_margins
        s.back = back_margins

    margin_params = sheet_template.create_parameters(final_page_size)

    for s in sheets:
        paste_to_margin(
            margin_params,
            s,
            (
                (final_page_size[0] - s.size[0]) // 2,
                (final_page_size[1] - s.size[1]) // 2,
            ),
        )

    return sheets


def create_cards(card_data: card.CardData) -> list[card.Card]:
    """Takes information from a CardData object and returns a list of Cards."""
    card_list = []

    for card_index in range(0, card_data.card_count):
        current_card = card.Card(
            assembly=card_data.assembly,
            bkt_hrs=card_data.bkt_hrs,
            bkt_qty=(
                card_data.remainder_parts
                if card_data.remainder_parts and card_index + 1 == card_data.card_count
                else card_data.bkt_qty
            ),
            card_count=card_data.card_count,
            card_num=card_index + 1,
            exp_vel=card_data.exp_vel,
            job_num=card_data.job_num,
            job_qty=card_data.job_qty,
            ops=card_data.ops,
            part_name=card_data.part_name,
            part_num=card_data.part_num,
            pro_date=card_data.pro_date,
        )

        card_list.append(current_card)
        card_index += 1

    return card_list


def create_card_data(
    quantities: dict[str, str], details: dict[str, str], ops: str
) -> card.CardData:
    """Create a new card.CardData object from form values."""
    qtys: dict = helpers.translate_dict_keys(quantities, (constants.FORM_TRANSLATIONS,))
    dtls: dict = helpers.translate_dict_keys(details, (constants.FORM_TRANSLATIONS,))
    ops: list = [i.strip().upper() for i in ops.split(",")]

    return card.CardData(**qtys, **dtls, ops=ops)


def export_cards(quantities: dict[str, str], details: dict[str, str], ops: str):
    """Run full card-creation process."""

    # show an error if required fields left blank
    if not quantities["Parts Per Bucket"]:
        messagebox.showerror("Required Field", '"Parts Per Bucket" cannot be empty.')
        return

    # show a warning for large part quantities
    if int(quantities["Total Parts"]) >= constants.LARGE_PART_QUANTITY:
        if not messagebox.askokcancel(
            "Warning: Total Parts",
            "Large part quantities can result in large documents and slow render times. Are you sure?",
        ):
            return

    sheet_template = sheet.SheetTemplate(constants.SHEET_SIZE)

    card_data: card.CardData = create_card_data(quantities, details, ops)
    card_list: list[card.Card] = create_cards(card_data)
    sheets = add_cards_to_sheets(sheet_template, card_list)

    add_uniform_margin(
        sheet_template,
        sheets,
        (int(sheet_template.size[0] * 1.1), int(sheet_template.size[1] * 1.1)),
    )

    job_num: str = card_data.job_num

    output_path = generate_page_images(job_num, sheets)
    output_file = generate_pdf(job_num, output_path)

    open_in_explorer(output_file)


def generate_page_images(
    output_dir_name: str, sheets: list[sheet.Sheet]
) -> pathlib.Path:
    """Create image files from list of Sheets and return the output path."""

    # export_time goes down to the second to prevent most permissions errors.
    export_time = datetime.now().strftime("%m.%d.%Y-%H.%M.%S")

    path = pathlib.Path(f"./output/{output_dir_name}-{export_time}")
    path.mkdir(parents=True, exist_ok=True)

    for page_num, s in enumerate(sheets):
        s.front.save(path / f"{page_num}-1.jpg")
        s.back.save(path / f"{page_num}-2.jpg")

    return path


def generate_pdf(filename: str, image_directory: pathlib.Path):
    """Generate the final PDF for printing and return the output file path."""
    image_paths = image_directory.glob("*.jpg")

    images = [Image.open(path) for path in image_paths]
    output_filename = f"{image_directory / filename}.pdf"

    # attach all pages to the first page
    first_page = images.pop(0)
    first_page.save(
        output_filename, "PDF", resolution=100.0, save_all=True, append_images=images
    )

    return output_filename


def import_data(
    widget_groups: tuple[helpers.LabeledWidgetGroup], text: tk.Text
) -> None:
    """Prompts user for a file, then fills GUI forms with its contents.

    Supported:
    - Excel (*.xlsx)
    """

    # TODO: Add support for CSV
    file_path = pathlib.Path(
        tkinter.filedialog.askopenfilename(
            title="Import Data",
            filetypes=(
                ("Excel Spreadsheet", "*.xlsx"),
                # ("Comma-Separated Values", "*.csv"),
            ),
        )
    )

    if file_path.suffix == ".xlsx":
        ws = file_import.load_excel(file_path)

        form_values = file_import.form_values_from_excel(ws)

        for group in widget_groups:
            form_values.fill_labeled_widget_group(group)

        form_values.fill_text_entry(text)


def open_in_explorer(path: pathlib.Path):
    subprocess.Popen(f'explorer "{path}"')
