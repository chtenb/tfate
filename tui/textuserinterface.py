"""This module contains the UserInterface class."""
from time import sleep
from threading import Thread
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

from . import utils


class TextUserInterface(UserInterface):

    """
    This class provides a user interface for interacting with a session object.
    """

    def __init__(self, stdscr, filename=''):
        # TODO: make stdscr global
        self.stdscr = stdscr
        self.session = Session(filename)
        self.session.ui = self
        self.session.OnQuit.add(self.quit)

        from . import HAS_COLORS, HAS_BACKGROUND_COLORS, COLOR_PAIRS
        self.has_colors = HAS_COLORS
        self.has_background_colors = HAS_BACKGROUND_COLORS
        self.color_pairs = COLOR_PAIRS

        self.refresh_rate = 30
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

    def touch(self):
        """Tell the screen thread to update the screen."""
        self.touched = True

    def activate(self):
        """Activate the user interface."""
        # First deactivate all other userinterfaces
        # When we allow splitscreens etc, this must be changed
        for session in session_list:
            session.ui.deactivate()
        self.active = True

        self.session_win.activate()
        self.text_win.activate()
        self.log_win.activate()
        self.clipboard_win.activate()
        self.undo_win.activate()
        self.status_win.activate()

        try:
            self.screen_thread = Thread(target=self._screen_loop)
            self.screen_thread.start()
            while self.active:
                self.touch()
                self.session.main()
        except:
            raise
        finally:
            self.deactivate()

    def deactivate(self):
        """Deactivate the user interface."""
        if self.active:
            self.active = False

            self.session_win.deactivate()
            self.text_win.deactivate()
            self.log_win.deactivate()
            self.clipboard_win.deactivate()
            self.undo_win.deactivate()
            self.status_win.deactivate()

            # Wait until screen thread is terminated,
            # to avoid having multiple threads writing to the screen
            #self.screen_thread.join()
            #self.log_win.logchecker_thread.join()

    def _screen_loop(self):
        """Loop that refreshes screen when touched."""
        while self.active:
            if self.touched:
                self.touched = False
                self._refresh()
            sleep(1 / self.refresh_rate)

    def _refresh(self):
        """Refresh all subwindows and stdscr."""
        self.text_win.refresh()
        self.clipboard_win.refresh()
        self.log_win.refresh()
        self.undo_win.refresh()
        self.status_win.refresh()
        self.session_win.refresh()
        self.command_win.refresh()

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
        # Intercept resize events
        if char == 'Resize':
            self._create_windows()
            self.touch()
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
