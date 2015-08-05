"Module containing ClipboardWin class."""
from .window import Window


class ClipboardWin(Window):
    """Window containing the clipboard"""

    def __init__(self, ui):
        Window.__init__(self, ui)

    def draw(self):
        """Draw clipboard"""
        caption = 'Clipboard'
        content = ', '.join(self.doc.clipboard.peek() or ['Empty'])
        stack = '-'.join('o' for x in self.doc.clipboard.storage)
        stacktail = stack[1 - self.width:]

        self.draw_line(caption, self.create_attribute(alt_background=True))
        self.draw_line(content)
        self.draw_line(stacktail)
