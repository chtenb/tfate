"""This module contains the UserInterface class."""
import unicurses as curses

from fate.session import Session, sessionlist
from fate.userinterface import UserInterface

from .sessionwin import SessionWin
from .textwin import TextWin
from .clipboardwin import ClipboardWin
from .undowin import UndoWin
from .statuswin import StatusWin
from .commandwin import CommandWin
from .logwin import LogWin
from . import utils, screen
from .terminal import stdscr

from logging import debug


class TextUserInterface(UserInterface):

    """
    This class provides a user interface for interacting with a session object.
    """

    def __init__(self, session):
        self.session = session
        self.active = False
        self.touched = False

        self._create_windows()

    def _create_windows(self):
        """Create all curses windows."""
        ymax, xmax = curses.getmaxyx(stdscr)
        self.session_win = SessionWin(xmax, 1, 0, 0, self)
        self.text_win = TextWin(xmax, ymax - 1 - 10 - 5 - 3 - 1, 0, 1, self)
        self.log_win = LogWin(xmax, 10, 0, ymax - 10 - 5 - 3 - 1, self)
        self.clipboard_win = ClipboardWin(xmax, 3, 0, ymax - 5 - 3 - 1, self)
        self.undo_win = UndoWin(xmax, 5, 0, ymax - 5 - 1, self)
        self.status_win = StatusWin(xmax, 1, 0, ymax - 1, self)

        self.command_win = CommandWin(int(xmax / 2), 2, int(xmax / 2), 4, self)

        self.windows = [self.session_win, self.text_win, self.log_win,
                        self.clipboard_win, self.undo_win, self.status_win,
                        self.command_win]

    def touch(self):
        """Tell the screen thread to update the screen."""
        self.touched = True

    def activate(self):
        """Activate the user interface."""
        screen.active_ui = self
        self.touch()

    def deactivate(self):
        """Deactivate the user interface."""
        screen.active_ui = None

    def refresh(self):
        """Refresh all windows."""
        for win in self.windows:
            win.refresh()

    def quit(self, session):
        """Activate next session, if existent."""
        assert session is self.session

        index = sessionlist.index(session)

        #debug(str(sessionlist))
        #debug("self: " + str(self.session))
        #debug("index: " + str(index))
        #self.getchar()

        if len(sessionlist) == 1:
            self.deactivate()
            return

        if index < len(sessionlist) - 1:
            next_session = sessionlist[index + 1]
        else:
            next_session = sessionlist[index - 1]

        #debug("next: " + str(next_session))
        next_session.ui.activate()

    def getchar(self):
        while 1:
            char = utils.getchar(stdscr)
            # Intercept resize events
            if char == 'Resize':
                self._create_windows()
                self.touch()
            else:
                return char

    def command_mode(self):
        self.command_win.prompt()

    def prompt(self, prompt_string='>'):
        """Prompt the user for an input string."""
        return self.status_win.prompt(prompt_string)

    def notify(self, message):
        self.status_win.set_status(message)
        self.getchar()
        self.status_win.set_default_status()

Session.default_userinterface = TextUserInterface
