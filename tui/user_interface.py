"""This module contains the UserInterface class."""
from fate.session import Session
from fate import modes
from . import key_mapping
import user
import curses
import sys
from .sessionwin import SessionWin
from .textwin import TextWin
from .clipboardwin import ClipboardWin
from .undowin import UndoWin
from .statuswin import StatusWin
from .commandwin import CommandWin
from logging import debug


class UserInterface:

    """This class provides a user interface for interacting with a session object."""

    def __init__(self):
        if len(sys.argv) > 1:
            self.session = Session(sys.argv[1])
        else:
            self.session = Session()
        self.session.read()
        self.session.search_pattern = ""
        self.mode = modes.SELECT_MODE

        # Load the right key mapping
        # User maps override the default maps
        self.action_keys = {}
        self.action_keys.update(key_mapping.action_keys)
        try:
            self.action_keys.update(user.action_keys)
        except AttributeError:
            pass

        self.ui_action_keys = {}
        self.ui_action_keys.update(key_mapping.ui_action_keys)
        try:
            self.ui_action_keys.update(user.ui_action_keys)
        except AttributeError:
            pass

    def main(self, stdscr):
        """Actually starts the user interface."""
        # Initialize color pairs from the terminal color palette
        # 0 is the default, 1-16 are the palette colors,
        # 17-32 are palette colors with a different background
        curses.use_default_colors()
        for i in range(0, 15):
            curses.init_pair(i + 1, i, -1)
            curses.init_pair(i + 17, i, 8)

        self.stdscr = stdscr
        curses.curs_set(0)
        self.stdscr.keypad(1)
        self.create_windows()

        # Enter the main loop
        while 1:
            if not self.session.interactionstack.isempty:
                self.mode = ' -> '.join(i.__name__ if hasattr(i, '__name__')
                                        else i.__class__.__name__
                                        for i in self.session.interactionstack.storage)
            else:
                self.mode = self.session.selection_mode
            self.status_win.set_default_status()
            self.normal_mode()
            self.refresh()

    def create_windows(self):
        """Create all curses windows."""
        ymax, xmax = self.stdscr.getmaxyx()
        self.session_win = SessionWin(xmax, 1, 0, 0, self.session, self)
        self.clipboard_win = ClipboardWin(xmax, 3, 0, ymax - 10, self.session)
        self.undo_win = UndoWin(xmax, 7, 0, ymax - 7, self.session)
        self.status_win = StatusWin(xmax, 1, 0, ymax - 1, self.session, self)
        self.command_win = CommandWin(int(xmax / 2), 2, int(xmax / 2), 4,
                                      self.session, self)
        self.text_win = TextWin(xmax, ymax - 7 - 3 - 1 - 1, 0, 1, self.session)

        self.stdscr.refresh()
        self.refresh()

    def refresh(self):
        """Refresh all subwindows."""
        self.text_win.refresh()
        self.clipboard_win.refresh()
        self.undo_win.refresh()
        self.status_win.refresh()
        self.session_win.refresh()

    def normal_mode(self):
        """We are in normal mode."""
        char = self.stdscr.get_wch()
        # debug(char)

        if char == curses.KEY_RESIZE:
            self.create_windows()
        elif not self.session.interactionstack.isempty:
            self.interactive_mode(char)
        elif char == ':':
            self.command_win.prompt()
        elif char in self.action_keys:
            action = self.action_keys[char]
            while callable(action):
                action = action(self.session)
        elif char in self.ui_action_keys:
            self.ui_action_keys[char](self)

    def interactive_mode(self, char):
        """We are in interactive mode."""
        session = self.session
        interaction = session.interactionstack.peek()

        if char == chr(27):
            # If escape is pressed, try to finish current action
            interaction.proceed(session)
            return
        elif char == curses.KEY_BACKSPACE:
            char = '\b'
        interaction.interact(session, char)

    def prompt(self, prompt_string='>'):
        """Prompt the user for an input string."""
        return self.status_win.prompt(prompt_string)


def publics(obj):
    """Return all object in __dir__ not starting with '_'"""
    return (name for name in dir(obj) if not name.startswith('_'))
