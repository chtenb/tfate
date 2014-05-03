"Module containing SessionWin class."""
from .win import Win
import curses


class SessionWin(Win):

    """Window displaying the headers of all current sessions."""

    def __init__(self, width, height, x, y, session, ui):
        Win.__init__(self, width, height, x, y, session)
        self.ui = ui
        self.set_background(self.colorpair(0, 1))

    def draw(self):
        """Draw the current session headers."""
        from fate.session import session_list
        for session in session_list:
            header = session.filename or '<nameless>'
            attributes = self.colorpair(14 if session is self.ui.session else 0, 1)
            self.draw_string(header + ' ', attributes)

