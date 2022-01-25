from PIL import Image


class SheetTemplate:
    def __init__(self, size: tuple[int]):
        self.size = size

        self.front = Image.new(*self.parameters)
        self.back = Image.new(*self.parameters)

    def add_card(self, card):
        self.front.paste(card.front_image, (self.current_x, self.current_y))

    @property
    def parameters(self) -> tuple:
        return ("RGB", self.size, "white")


class Sheet:
    back: Image
    front: Image
    size: tuple[int]
    template: SheetTemplate

    def __init__(self, template):
        self.template = template
        self.back = Image.new(*self.template.parameters)
        self.front = Image.new(*self.template.parameters)
        self.size = self.template.size

    def show(self):
        self.front.show()
        self.back.show()
