"Module containing ClipboardWin class."""
import curses
from .win import Win


class ClipboardWin(Win):
    """Window containing the clipboard"""

    def __init__(self, width, height, x, y, session):
        Win.__init__(self, width, height, x, y, session)

    def draw(self):
        """Draw clipboard"""
        try:
            self.win.addstr(0, 0, 'Clipboard: ' + self.session.clipboard.dump())
        except curses.error:
            # End of window reached
            pass
        self.win.clrtobot()
        self.win.refresh()
