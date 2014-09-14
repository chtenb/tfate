"Module containing DocumentWin class."""
from .window import Window


class DocumentWin(Window):

    """Window displaying the headers of all current documents."""

    def __init__(self, width, height, x, y, ui):
        Window.__init__(self, width, height, x, y, ui)

    def draw(self):
        """Draw the current document headers."""
        background = self.create_attribute(alt_background=True)
        highlight = self.create_attribute(highlight=True, alt_background=True)

        from fate.document import documentlist
        for document in documentlist:
            header = document.filename or '<nameless>'
            if document is self.ui.document:
                self.draw_string(header, highlight)
            else:
                self.draw_string(header, background)
            self.draw_string(' ', background)

        # Fill the rest of the line with alt_background
        self.draw_line('', self.create_attribute(alt_background=True))

