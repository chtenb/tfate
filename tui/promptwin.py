"Module containing StatusWin class."""
from .window import Window
from logging import debug
from fate.prompt import Prompt


class PromptWin(Window):

    """
    Window for drawing the user input prompt when in prompt mode.
    """

    def __init__(self, ui):
        Window.__init__(self, ui)

    def update(self):
        """We only want to be enabled if undomode is active."""
        if isinstance(self.document.mode, Prompt) and not self.enabled:
            self.enable()
        if not isinstance(self.document.mode, Prompt) and self.enabled:
            self.disable()

    def draw(self):
        text = self.document.mode.promptstring + self.document.mode.inputstring
        height = int(min(1, len(text)) / min(1, self.width))
        self.setdimensions(height=height)
        self.draw_line(text, self.create_attribute(alt_background=True))
