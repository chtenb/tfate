"""This module contains the UserInterface class."""
from fate.session import Session
from fate import actors, selectors, operators, modes
from fate.operation import Operation
from . import key_mapping
import user
import curses
import sys
from .textwin import TextWin
from .clipboardwin import ClipboardWin
from .actionwin import ActionWin
from .statuswin import StatusWin
from .commandwin import CommandWin
import logging
from rlcompleter import Completer


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
        self.create_windows()

        # Enter the main loop
        while 1:
            self.mode = self.session.selection_mode
            if self.session.insertoperation:
                #self.mode = 'INSERT'
                self.mode = self.session.insertoperation.__class__.__name__
            self.text_win.refresh()
            self.clipboard_win.refresh()
            self.actiontree_win.refresh()
            self.status_win.draw_default_status()
            self.status_win.refresh()

            self.normal_mode()

    def create_windows(self):
        """Create all curses windows."""
        ymax, xmax = self.stdscr.getmaxyx()
        self.text_win = TextWin(xmax, ymax - 10, 0, 0, self.session)
        self.clipboard_win = ClipboardWin(xmax, 3, 0, ymax - 10, self.session)
        self.actiontree_win = ActionWin(xmax, 7, 0, ymax - 7, self.session)
        self.status_win = StatusWin(xmax, 1, 0, ymax - 1, self.session, self)
        self.command_win = CommandWin(int(xmax/2), 2, int(xmax/2), 4, self.session, self)
        self.stdscr.refresh()

    def refesh(self):
        self.text_win.refresh()
        self.clipboard_win.refresh()
        self.actiontree_win.refresh()
        self.status_win.refresh()

    def normal_mode(self):
        """We are in normal mode."""
        char = chr(self.stdscr.getch())

        if char == chr(curses.KEY_RESIZE):
            self.create_windows()
        elif self.session.insertoperation:
            self.insert_mode(char)
        elif char == ':':
            self.command_win.prompt()
        elif char in self.action_keys:
            self.action_keys[char](self.session)
        elif char in self.ui_action_keys:
            self.ui_action_keys[char](self)

    def insert_mode(self, char):
        """We are in insert mode."""
        session = self.session

        if char == chr(27):
            session.insertoperation.done()
            return
        elif char == chr(curses.KEY_BACKSPACE):
            char = '\b'
        session.insertoperation.feed(char)
        self.text_win.refresh()

    def prompt(self, prompt_string='>'):
        """Prompt the user for an input string."""
        return self.status_win.prompt(prompt_string)

def publics(obj):
    """Return all object in __dir__ not starting with '_'"""
    return (name for name in dir(obj) if not name.startswith('_'))

