"Module containing StatusWin class."""
import curses
from .win import Win
from curses.textpad import Textbox


class StatusWin(Win):
    """Window containing the status."""

    def __init__(self, width, height, x, y, session, ui):
        Win.__init__(self, width, height, x, y, session)
        self.ui = ui

    def draw(self):
        """Draw the current status."""
        self.set_status(self.session.filename
                        + ("*" if not self.session.saved else "")
                        + " | " + str(self.session.filetype)
                        + " | " + self.ui.mode
                        + " | " + str(self.session.selection))

    def set_status(self, string):
        """Set the content of the status window."""
        self.win.bkgd(' ', curses.color_pair(17))
        self.draw_string(string, curses.color_pair(17))
        self.win.clrtobot()
        self.win.refresh()

    def prompt(self, prompt_string='>'):
        """Prompt the user for an input string."""
        self.win.erase()
        self.win.refresh()
        prompt_len = len(prompt_string)
        text_box_win = curses.newwin(1, self.width - prompt_len,
                                     self.y, self.x + prompt_len)
        text_box_win.bkgd(' ', curses.color_pair(17))
        text_box = Textbox(text_box_win)
        text_box.edit()
        return text_box.gather()[:-1]
