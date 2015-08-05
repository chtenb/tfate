"Module containing StatusWin class."""
from .window import Window


class StatusWin(Window):

    """Window containing the status."""

    def __init__(self, ui):
        Window.__init__(self, ui)

    def draw(self):
        """Draw the current status."""
        self.set_default_status()
        attribute = self.create_attribute(alt_background=True)
        self.draw_line(self.status, attribute)

    def set_default_status(self):
        """Set the status to the default value."""
        self.default_status = True
        doc = self.doc

        mode = str(doc.mode)
        selectmode = doc.selectmode

        string = '{}{} | {} | {} | {} | {}'.format(
            doc.filename,
            ('*' if not doc.saved else ''),
            doc.filetype,
            mode,
            selectmode,
            doc.selection)
        self.set_status(string)

    def set_status(self, string):
        """Set the status to the given string."""
        self.default_status = False
        self.status = string

    def prompt(self, prompt_string='>'):
        """Prompt the user for an input string."""
        self.set_status(prompt_string)
        self.ui.touch()

        string = ''
        while 1:
            key = self.ui.getkey()
            if key == 'Esc':
                self.set_default_status()
                return None
            elif key == '\n':
                self.set_default_status()
                return string
            elif key == '\b':
                if len(string) > 0:
                    string = string[:-1]
            else:
                string += key
            self.set_status(prompt_string + string)
            self.ui.touch()
