"""Module containing logging window."""
from .window import Window
import fate_logger

class LogWin(Window):

    """
    This window acts as a logging handler by storing all incoming records into list,
    which is printed on the screen in the draw method of this window.
    """

    def __init__(self, ui):
        Window.__init__(self, ui)

    def draw(self):
        """Draw log"""
        for r in fate_logger.RECORDS[-self.height:]:
            self.draw_line(r.message, self.create_attribute(reverse=True))
