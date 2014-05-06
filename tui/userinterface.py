"""This module contains the UserInterface class."""
from time import sleep
from threading import Thread

from fate.session import Session, session_list

from .sessionwin import SessionWin
from .textwin import TextWin
from .clipboardwin import ClipboardWin
from .undowin import UndoWin
from .statuswin import StatusWin
from .commandwin import CommandWin
from .logwin import LogWin

from . import utils


class UserInterface:

    """
    This class provides a user interface for interacting with a session object.
    """

    def __init__(self, stdscr, filename=''):
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
        ymax, xmax = self.stdscr.getmaxyx()
        self.session_win = SessionWin(xmax, 1, 0, 0, self.session)
        self.text_win = TextWin(xmax, ymax - 1 - 3 - 3 - 7 - 1, 0, 1, self.session)
        self.log_win = LogWin(xmax, 3, 0, ymax - 14, self.session)
        self.clipboard_win = ClipboardWin(xmax, 3, 0, ymax - 11, self.session)
        self.undo_win = UndoWin(xmax, 7, 0, ymax - 8, self.session)
        self.status_win = StatusWin(xmax, 1, 0, ymax - 1, self.session)
        self.command_win = CommandWin(int(xmax / 2), 2, int(xmax / 2), 4,
                                      self.session, self)

    def __enter__(self):
        """When activated, we start a screen refresh thread."""
        self.screen_thread = Thread(target=self._refresh_screen_loop)
        self.screen_thread.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.deactivate()

    def touch(self):
        """Tell the screen thread to update the screen."""
        self.touched = True

    def activate(self):
        """Activate the user interface."""
        self.active = True

        with self:
            while self.active:
                self.touch()
                self.session.main()

    def deactivate(self):
        """Deactivate the user interface."""
        self.active = False
        # Wait until screen thread is terminated,
        # to avoid having multiple threads writing to the screen
        self.screen_thread.join()

    def _refresh_screen_loop(self):
        """Loop that refreshes screen when touched."""
        while self.active:
            if self.touched:
                self.touched = False
                self._refresh()
            sleep(0.01)

    def _refresh(self):
        """Refresh all subwindows."""
        self.text_win.refresh()
        self.clipboard_win.refresh()
        self.log_win.refresh()
        self.undo_win.refresh()
        self.status_win.refresh()
        self.session_win.refresh()
        self.command_win.refresh()

        self.stdscr.refresh()

    def quit(self, session):
        """Activate next session, if existent."""
        assert session is self.session

        index = session_list.index(session)
        if len(session_list) == 1:
            return

        if index < len(session_list) - 1:
            next_session = session_list[index]
        else:
            next_session = session_list[index - 1]

        self.deactivate()
        next_session.ui.activate()

    def getchar(self):
        char = utils.getchar(self.stdscr)
        if char == 'Resize':
            self._create_windows()
            self.touch()
        return char


    def prompt(self, prompt_string='>'):
        """Prompt the user for an input string."""
        return self.status_win.prompt(prompt_string)
