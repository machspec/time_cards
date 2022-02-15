from app import constants
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont

import math


@dataclass
class Card:
    """Contains information for a single card."""

    card_count: str
    card_num: str

    assembly: str
    bkt_hrs: str
    bkt_qty: str
    exp_vel: str
    job_num: str
    job_qty: str
    ops: list[str]
    part_name: str
    part_num: str
    pro_date: str

    front_image: Image = None
    back_image: Image = None

    def build_front_image(self):
        """Put front images together."""
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
        self.place_text(front_output, self.job_qty, (307, 78))
        self.place_text(front_output, self.bkt_hrs, (497, 78))
        self.place_text(front_output, self.assembly, (700, 78))

        self.place_operations_text(front_output, self.ops)

        self.front_image = front_output

    def build_back_image(self):
        """Put back images together."""
        card_back = Image.open("./app/resources/card_back.jpg")

        back_output = card_back.copy()

        # place text on back image
        self.place_text(back_output, self.job_num, (53, 6))
        self.place_text(back_output, self.card_num, (357, 6))

        self.place_text(back_output, self.part_num, (80, 43))
        self.place_text(back_output, self.part_name, (82, 76))
        self.place_text(back_output, self.assembly, (67, 112))

        self.place_text(back_output, self.job_qty, (104, 146))
        self.place_text(back_output, self.pro_date, (120, 182))

        self.back_image = back_output

    def build_card(self):
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

    assembly: str
    bkt_hrs: str
    bkt_qty: int
    exp_vel: str
    job_num: str
    part_name: str
    part_num: str
    part_qty: int
    pro_date: str

    ops: list[str] = None

    def __post_init__(self):
        self.bkt_qty = int(self.bkt_qty)
        self.part_qty = int(self.part_qty)

        self.job_qty = self.part_qty

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
