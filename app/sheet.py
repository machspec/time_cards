from PIL import Image


class SheetTemplate:
    """Base class that holds information for `Sheet` creation."""

    def __init__(self, size: tuple[int]):
        self.size = size

    @property
    def parameters(self) -> tuple:
        """Returns a tuple of parameters `("RGB", self.size, "white")`."""
        return ("RGB", self.size, "white")

    def create_parameters(self, size: tuple[int]) -> tuple:
        """Returns a tuple of parameters `("RGB", size, "white")`."""
        return ("RGB", size or self.size, "white")


class Sheet:
    """Container for two equally-sized Image items, front and back."""

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
        """Calls `Image.show()` for front and back."""
        self.front.show()
        self.back.show()
