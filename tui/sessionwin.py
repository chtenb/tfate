"Module containing SessionWin class."""
from .win import Win


class SessionWin(Win):

    """Window displaying the headers of all current sessions."""

    def __init__(self, width, height, x, y, session, ui):
        Win.__init__(self, width, height, x, y, session)
        self.ui = ui

    def draw(self):
        """Draw the current session headers."""
        from fate.session import session_list
        for session in session_list:
            header = session.filename or '<nameless>'
            highlight = True if session is self.ui.session else False
            attributes = self.create_attribute(highlight=highlight, alt_background=True)
            self.draw_string(header + ' ', attributes)

