"Module containing ClipboardWin class."""
from .win import Win


class ClipboardWin(Win):
    """Window containing the clipboard"""

    def __init__(self, width, height, x, y, session):
        Win.__init__(self, width, height, x, y, session)

    def draw(self):
        """Draw clipboard"""
        caption = 'Clipboard'
        content = ', '.join(self.session.clipboard.peek() or ['Empty'])
        stack = '-'.join('o' for x in self.session.clipboard.storage)
        stacktail = stack[1 - self.width:]

        self.draw_line(caption, self.colorpair(0, 1))
        self.draw_line(content)
        self.draw_line(stacktail)
