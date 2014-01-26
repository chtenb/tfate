"Module containing ActionWin class."""
import curses
from .win import Win


class ActionWin(Win):
    """Window containing the actiontree."""

    def __init__(self, width, height, x, y, session):
        Win.__init__(self, width, height, x, y, session)

    def draw(self):
        """Draw the current actiontree."""
        try:
            self.win.addstr(0, 0, 'History:\n' + self.session.actiontree.dump())
        except curses.error:
            # End of window reached
            pass
        self.win.clrtobot()
        self.win.refresh()
