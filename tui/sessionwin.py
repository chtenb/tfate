"Module containing SessionWin class."""
import curses
from .win import Win


class SessionWin(Win):

    """Window displaying the headers of all current sessions."""

    def __init__(self, width, height, x, y, session, ui):
        Win.__init__(self, width, height, x, y, session)
        self.ui = ui
        self.set_background(curses.color_pair(17))

    def draw(self):
        """Draw the current session headers."""
        from fate.session import session_list
        for session in session_list:
            header = session.filename or '<nameless>'
            color = 31 if session is self.ui.session else 17
            self.draw_string(header + ' ', curses.color_pair(color))

