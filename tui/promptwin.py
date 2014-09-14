"Module containing StatusWin class."""
from .window import Window
from logging import debug
from fate.prompt import Prompt


class PromptWin(Window):

    """
    Window for drawing the user input prompt when in prompt mode.
    """

    def __init__(self, width, height, x, y, ui):
        Window.__init__(self, width, height, x, y, ui)
        self.min_height = height

    def draw(self):
        if self.document.mode and isinstance(self.document.mode.peek(), Prompt):
            text = self.document.mode.peek().inputstring
            self.height = max(self.min_height, int(len(text) / self.width))
            self.draw_line(text, self.create_attribute(alt_background=True))

