"""This module contains the UserInterface class."""
from time import sleep
from threading import Thread

from fate.session import Session, session_list
from fate import modes

from logging import debug

from .sessionwin import SessionWin
from .textwin import TextWin
from .clipboardwin import ClipboardWin
from .undowin import UndoWin
from .statuswin import StatusWin
from .commandwin import CommandWin
from .logwin import LogWin

from . import utils


class UserInterface:

    """This class provides a user interface for interacting with a session object."""

    def __init__(self, stdscr, filename=''):
        self.stdscr = stdscr
        self.session = Session(filename)
        self.session.ui = self
        self.session.OnQuit.add(self.exit)

        from . import HAS_COLORS, HAS_BACKGROUND_COLORS, COLOR_PAIRS
        self.has_colors = HAS_COLORS
        self.has_background_colors = HAS_BACKGROUND_COLORS
        self.color_pairs = COLOR_PAIRS

        self.need_refresh = False
        self.running = False
        self.mode = modes.SELECT_MODE

    def touch(self):
        self.need_refresh = True

    def activate(self):
        """Activate the user interface."""

        # TODO: use context managers to close threads automatically
        # E.g. after a crash

        self.create_windows()

        def refresh_screen():
            """Main loop that refreshes screen when touched."""
            self.running = True
            while self.running:
                if self.need_refresh:
                    self.need_refresh = False
                    self.refresh()
                sleep(0.1)
        ui_thread = Thread(target=refresh_screen)
        ui_thread.start()

        while 1:
            self.normal_mode()
            self.touch()

    def create_windows(self):
        """Create all curses windows."""
        ymax, xmax = self.stdscr.getmaxyx()
        self.session_win = SessionWin(xmax, 1, 0, 0, self.session)
        self.clipboard_win = ClipboardWin(xmax, 3, 0, ymax - 10, self.session)
        self.undo_win = UndoWin(xmax, 7, 0, ymax - 7, self.session)
        self.status_win = StatusWin(xmax, 1, 0, ymax - 1, self.session)
        self.command_win = CommandWin(int(xmax / 2), 2, int(xmax / 2), 4,
                                      self.session, self)
        self.text_win = TextWin(xmax, ymax - 7 - 3 - 1 - 1 - 5, 0, 1, self.session)
        self.log_win = LogWin(xmax, 15, 0, ymax - 25, self.session)

        self.stdscr.refresh()
        self.refresh()

    def refresh(self):
        """Refresh all subwindows."""
        self.text_win.refresh()
        self.clipboard_win.refresh()
        self.log_win.refresh()
        self.undo_win.refresh()
        self.status_win.refresh()
        self.session_win.refresh()

    def exit(self, session):
        """Activate next session, if existent."""
        assert session is self.session

        index = session_list.index(session)
        if len(session_list) == 1:
            return

        if index < len(session_list) - 1:
            next_session = session_list[index]
        else:
            next_session = session_list[index - 1]

        self.running = False
        next_session.ui.activate()

    def getchar(self):
        char = utils.getchar(self.stdscr)
        if char == 'Resize':
            self.create_windows()
        return char

    def normal_mode(self):
        """We are in normal mode."""
        char = self.getchar()

        if not self.session.interactionstack.isempty:
            self.interactive_mode(char)
        elif char == ':':
            self.command_win.prompt()
        elif char in self.session.keymap:
            action = self.session.keymap[char]
            while callable(action):
                action = action(self.session)

    def interactive_mode(self, char):
        """We are in interactive mode."""
        session = self.session
        interaction = session.interactionstack.peek()

        if char == 'Esc':
            interaction.proceed(session)
        else:
            interaction.interact(session, char)

    def prompt(self, prompt_string='>'):
        """Prompt the user for an input string."""
        return self.status_win.prompt(prompt_string)
