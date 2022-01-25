from PIL import Image


class SheetTemplate:
    def __init__(self, size: tuple[int], margin_x: int = 0, margin_y: int = 0):
        self.size = size
        self.margin_x = margin_x
        self.margin_y = margin_y

        self.front = Image.new("RGB", self.size, "white")
        self.back = Image.new("RGB", self.size, "white")

    def add_card(self, card):
        self.front.paste(card.front_image, (self.current_x, self.current_y))

    @property
    def current_x(self):
        return 0

    @property
    def current_y(self):
        return 0
