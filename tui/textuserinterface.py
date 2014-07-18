"""This module contains the UserInterface class."""
import unicurses as curses

from fate.session import Session, session_list
from fate.userinterface import UserInterface

from .sessionwin import SessionWin
from .textwin import TextWin
from .clipboardwin import ClipboardWin
from .undowin import UndoWin
from .statuswin import StatusWin
from .commandwin import CommandWin
from .logwin import LogWin
from . import screen

from . import utils
from logging import debug


class TextUserInterface(UserInterface):

    """
    This class provides a user interface for interacting with a session object.
    """

    def __init__(self, stdscr, filename=''):
        # TODO: maybe remove stdscr as a member
        self.stdscr = stdscr
        self.session = Session(filename)
        self.session.ui = self
        self.session.OnQuit.add(self.quit)

        from . import HAS_COLORS, HAS_BACKGROUND_COLORS, COLOR_PAIRS
        self.has_colors = HAS_COLORS
        self.has_background_colors = HAS_BACKGROUND_COLORS
        self.color_pairs = COLOR_PAIRS

        self.active = False
        self.touched = False

        self._create_windows()

    def _create_windows(self):
        """Create all curses windows."""
        ymax, xmax = curses.getmaxyx(self.stdscr)
        self.session_win = SessionWin(xmax, 1, 0, 0, self.session)
        self.text_win = TextWin(xmax, ymax - 1 - 10 - 3 - 3 - 1, 0, 1, self.session)
        self.log_win = LogWin(xmax, 10, 0, ymax - 10 - 3 - 3 - 1, self.session)
        self.clipboard_win = ClipboardWin(xmax, 3, 0, ymax - 3 - 3 - 1, self.session)
        self.undo_win = UndoWin(xmax, 3, 0, ymax - 3 - 1, self.session)
        self.status_win = StatusWin(xmax, 1, 0, ymax - 1, self.session)

        self.command_win = CommandWin(int(xmax / 2), 2, int(xmax / 2), 4,
                                      self.session, self)

        self.windows = [self.session_win, self.text_win, self.log_win,
                        self.clipboard_win, self.undo_win, self.status_win,
                        self.command_win]

    def touch(self):
        """Tell the screen thread to update the screen."""
        self.touched = True

    def activate(self):
        """Activate the user interface."""
        # First deactivate all other userinterfaces
        # When we allow splitscreens etc, this must be changed
        #for session in session_list:
            #session.ui.deactivate()
        screen.active_ui = self
        self.touch()

    def deactivate(self):
        """Deactivate the user interface."""
        screen.active_ui = None
        #if self.active:
            #self.active = False

            # Wait until screen thread is terminated,
            # to avoid having multiple threads writing to the screen
            # self.screen_thread.join()
            # self.log_win.logchecker_thread.join()

    def refresh(self):
        """Refresh all windows."""
        for win in self.windows:
            win.refresh()

    def quit(self, session):
        """Activate next session, if existent."""
        assert session is self.session

        index = session_list.index(session)

        debug(str(session_list))
        debug("self: " + str(self.session))
        debug("index: " + str(index))
        #self.getchar()

        if len(session_list) == 1:
            self.deactivate()
            return

        if index < len(session_list) - 1:
            next_session = session_list[index + 1]
        else:
            next_session = session_list[index - 1]

        debug("next: " + str(next_session))
        next_session.ui.activate()

    def getchar(self):
        while 1:
            char = utils.getchar(self.stdscr)
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
