"""This module contains the UserInterface class."""
from fate.session import Session
from fate import modes
import user
import curses
from .sessionwin import SessionWin
from .textwin import TextWin
from .clipboardwin import ClipboardWin
from .undowin import UndoWin
from .statuswin import StatusWin
from .commandwin import CommandWin
from logging import debug

ui_list = []


class UserInterface:

    """This class provides a user interface for interacting with a session object."""

    def __init__(self, stdscr, filename=''):
        ui_list.append(self)
        self.stdscr = stdscr
        self.session = Session(filename)

        self.session.search_pattern = ""
        self.mode = modes.SELECT_MODE

        # Load the right key mapping
        # User maps override the default maps
        # TODO: allow filetype dependent mapping changes
        from . import key_mapping
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

    def activate(self):
        """Activate the user interface."""
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

    def exit(self):
        """Exit userinterface and corresponding session."""
        self.session.exit()
        index = ui_list.index(self)
        del ui_list[index]
        if index < len(ui_list):
            ui_list[index].activate()
        elif 0 <= index - 1:
            ui_list[index - 1].activate()
        else:
            exit()

    def getkey(self):
        """
        Wait for the user to press a key and convert it to a string.
        """
        while 1:
            try:
                char = self.stdscr.get_wch()
            except curses.error:
                pass
            else:
                # Modify if ctrl was pressed
                char = curses.unctrl(char)
                # Return char as a string
                return char.decode()

    def normal_mode(self):
        """We are in normal mode."""
        char = self.getkey()

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
