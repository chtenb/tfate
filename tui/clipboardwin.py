"Module containing ClipboardWin class."""
from .win import Win


class ClipboardWin(Win):
    """Window containing the clipboard"""

    def __init__(self, width, height, x, y, ui):
        Win.__init__(self, width, height, x, y, ui)

    def draw(self):
        """Draw clipboard"""
        caption = 'Clipboard'
        content = ', '.join(self.session.clipboard.peek() or ['Empty'])
        stack = '-'.join('o' for x in self.session.clipboard.storage)
        stacktail = stack[1 - self.width:]

        self.draw_line(caption, self.create_attribute(alt_background=True))
        self.draw_line(content)
        self.draw_line(stacktail)
