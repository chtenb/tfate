"Module containing ClipboardWin class."""
import curses
from .win import Win


class ClipboardWin(Win):
    """Window containing the clipboard"""

    def __init__(self, width, height, x, y, session):
        Win.__init__(self, width, height, x, y, session)

    def draw(self):
        """Draw clipboard"""
        string = '-'.join('o' for x in self.session.clipboard.storage)
        try:
            self.win.addstr(0, 0, 'Clipboard: ' + string)
        except curses.error:
            # End of window reached
            pass
        Win.draw(self)
