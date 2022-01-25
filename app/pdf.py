from typing import Any
from app import sheet
from dataclasses import dataclass
from reportlab.platypus import Image, PageBreak, SimpleDocTemplate
from reportlab.pdfgen import canvas
from typing import Any

import pathlib


@dataclass
class PDF(SimpleDocTemplate):
    path: str
    size: tuple[int]

    contents: list[Any] = None

    def __init__(self, path: str, pagesize: tuple[int]):
        super().__init__(path, pagesize=pagesize)

    def add_image_as_page(self, image_path: pathlib.Path):
        if self.contents is None:
            self.contents = []

        self.contents.append(Image(image_path))

    def build_contents(self):
        self.build(self.contents)
