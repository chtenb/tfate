"Module containing SessionWin class."""
from .win import Win


class SessionWin(Win):

    """Window displaying the headers of all current sessions."""

    def __init__(self, width, height, x, y, ui):
        Win.__init__(self, width, height, x, y, ui)

    def draw(self):
        """Draw the current session headers."""
        background = self.create_attribute(alt_background=True)
        highlight = self.create_attribute(highlight=True, alt_background=True)

        from fate.session import sessionlist
        for session in sessionlist:
            header = session.filename or '<nameless>'
            if session is self.ui.session:
                self.draw_string(header, highlight)
            else:
                self.draw_string(header, background)
            self.draw_string(' ', background)

        # Fill the rest of the line with alt_background
        self.draw_line('', self.create_attribute(alt_background=True))

