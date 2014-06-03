"Module containing StatusWin class."""
import unicurses as curses
from .win import Win


class StatusWin(Win):

    """Window containing the status."""

    def __init__(self, width, height, x, y, session):
        Win.__init__(self, width, height, x, y, session)
        self.set_default_status()

    def draw(self):
        """Draw the current status."""
        attribute = self.create_attribute(alt_background=True)
        self.draw_line(self.status, attribute)
        self.set_default_status()

    def set_default_status(self):
        """Set the status to the default value."""
        session = self.session

        #if not session.interactionstack.isempty:
            #mode = ' -> '.join(i.__name__ if hasattr(i, '__name__')
                               #else i.__class__.__name__
                               #for i in session.interactionstack.storage)
        #else:
        mode = session.selection_mode

        string = '{}{} | {} | {} | {}'.format(
            session.filename,
            ('*' if not self.session.saved else ''),
            session.filetype,
            mode,
            session.selection)
        self.status = string

    def set_status(self, string):
        """Set the status to the given string."""
        self.status = string

    def prompt(self, prompt_string='>'):
        """Prompt the user for an input string."""
        attribute = self.create_attribute(alt_background=True)
        curses.werase(self.win)
        self.draw_string(prompt_string, attribute)
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
            self.status = prompt_string + string
            self.ui.touch()
