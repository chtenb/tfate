"Module containing StatusWin class."""
import curses
from .win import Win
from curses.textpad import Textbox


class StatusWin(Win):
    """Window containing the status."""

    def __init__(self, width, height, x, y, session):
        Win.__init__(self, width, height, x, y, session)
        self.set_default_status()

    def draw(self):
        """Draw the current status."""
        attribute = self.create_attribute(alt_background=True)
        self.draw_line(self.status, attribute)

    def set_default_status(self):
        """Set the status to the default value."""
        self.status = (self.session.filename
                       + ("*" if not self.session.saved else "")
                       + " | " + str(self.session.filetype)
                       + " | " + self.ui.mode
                       + " | " + str(self.session.selection))
        self.refresh()

    def draw_status(self, string):
        """Set the status to the given string."""
        self.status = string
        self.refresh()

    def prompt(self, prompt_string='>'):
        """Prompt the user for an input string."""
        attribute = self.create_attribute(alt_background=True)
        self.win.erase()
        self.draw_string(prompt_string, attribute)
        self.win.refresh()
        prompt_len = len(prompt_string)
        text_box_win = curses.newwin(1, self.width - prompt_len,
                                     self.y, self.x + prompt_len)
        text_box_win.bkgd(' ', attribute)
        text_box = Textbox(text_box_win)
        text_box.edit()
        return text_box.gather()[:-1]
