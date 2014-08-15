"Module containing StatusWin class."""
import unicurses as curses
from .win import Win


class StatusWin(Win):

    """Window containing the status."""

    default_status = True

    def __init__(self, width, height, x, y, ui):
        Win.__init__(self, width, height, x, y, ui)

    def draw(self):
        """Draw the current status."""
        # If we were displaying default status anyway, keep it up to date
        # Make sure alternative messages last only one touch
        if self.default_status:
            self.set_default_status()
        else:
            self.default_status = True

        attribute = self.create_attribute(alt_background=True)
        self.draw_line(self.status, attribute)

    def set_default_status(self):
        """Set the status to the default value."""
        self.default_status = True
        document = self.document

        #if not document.intercommandstack.isempty:
            #mode = ' -> '.join(i.__name__ if hasattr(i, '__name__')
                               #else i.__class__.__name__
                               #for i in document.intercommandstack.storage)
        #else:

        string = '{}{} | {} | {} | {}'.format(
            document.filename,
            ('*' if not self.document.saved else ''),
            document.filetype,
            document.mode,
            document.selection)
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
            char = self.ui.getchar()
            if char == 'Esc':
                self.set_default_status()
                return None
            elif char == '\n':
                self.set_default_status()
                return string
            elif char == '\b':
                if len(string) > 0:
                    string = string[:-1]
            else:
                string += char
            self.set_status(prompt_string + string)
            self.ui.touch()
