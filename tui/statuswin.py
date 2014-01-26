"Module containing StatusWin class."""
import curses
from .win import Win
from curses.textpad import Textbox


class StatusWin(Win):
    """Window containing the status."""

    def __init__(self, width, height, x, y, session):
        Win.__init__(self, width, height, x, y, session)

    def draw(self, mode):
        """Draw the current status."""
        self.set_status(self.session.filename
                        + ("*" if not self.session.saved else "")
                        + " | " + str(self.session.filetype)
                        + " | " + mode
                        + " | " + str(self.session.selection))

    def set_status(self, string):
        """Set the content of the status window."""
        self.win.bkgd(' ', curses.color_pair(9))
        try:
            self.win.addstr(0, 0, string, curses.color_pair(9))
        except curses.error:
            # End of window reached
            pass
        self.win.clrtobot()
        self.win.refresh()

    def prompt(self, prompt_string='>'):
        """Prompt the user for an input string."""
        self.win.erase()
        ymax, xmax = self.win.getmaxyx()
        y, x = self.win.getbegyx()
        self.win.addstr(0, 0, prompt_string)
        self.win.refresh()
        prompt_len = len(prompt_string)
        text_box_win = curses.newwin(1, xmax - prompt_len, y, x + prompt_len)
        text_box_win.bkgd(' ', curses.color_pair(9))
        text_box = Textbox(text_box_win)
        text_box.edit()
        return text_box.gather()[:-1]
