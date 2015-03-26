"""Module containing ErrorWin class."""
from .window import Window
from fate.errorchecking import ErrorMode
from fate.navigation import position_to_coord
from logging import debug


class ErrorWin(Window):

    """Window containing the errors."""

    def __init__(self, ui):
        Window.__init__(self, ui)

    def update(self):
        """We only want to be enabled if errormode is active."""
        if isinstance(self.document.mode, ErrorMode) and not self.enabled:
            self.enable()
        if not isinstance(self.document.mode, ErrorMode) and self.enabled:
            self.disable()

    def draw(self):
        errorlist = self.document.errorlist

        self.draw_line('Error list', self.create_attribute(alt_background=True))

        for i, (errortype, interval, message) in enumerate(errorlist):
            attribute = self.create_attribute()
            if self.document.errorlist.current == i:
                attribute = self.create_attribute(reverse=True)
            line, column = position_to_coord(interval[0], self.document.text)
            self.draw_line('{} at {},{}: {}'.format(errortype, line, column, message),
                           attribute)
