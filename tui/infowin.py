"Module containing StatusWin class."""
from .window import Window


class InfoWin(Window):

    """Window for displaying a message."""

    def __init__(self, width, height, x, y, ui):
        Window.__init__(self, width, height, x, y, ui)
        self.message = ''

    def draw(self):
        """Draw the current message."""
        if self.message:
            attribute = self.create_attribute(alt_background=True)
            self.draw_line(self.message, attribute)

    def set_message(self, string):
        """Set the message to the given string."""
        self.message = string

    def del_message(self):
        """Delete the message."""
        self.message = ''

