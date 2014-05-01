"""This module contains the UserInterface class."""
from fate.session import Session, session_list
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


class UserInterface:

    """This class provides a user interface for interacting with a session object."""

    def __init__(self, stdscr, filename=''):
        self.stdscr = stdscr
        self.session = Session(filename)
        self.session.ui = self
        self.session.OnQuit.add(self.exit)

        self.session.search_pattern = ""
        self.mode = modes.SELECT_MODE

        # Load the right key mapping
        # User maps override the default maps
        # TODO: allow filetype dependent mapping changes
        from fate import key_mapping
        self.session.key_mapping = {}
        self.session.key_mapping.update(key_mapping.action_keys)
        try:
            self.session.key_mapping.update(user.action_keys)
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
        next_session.ui.activate()

    def getchar(self):
        """Retrieve input character from user as a readable string."""
        while 1:
            try:
                char = self.stdscr.get_wch()
                break
            except curses.error:
                pass

        if isinstance(char, str):
            _ord = ord(char)

            # Replace special characters with a readable string
            if _ord == 27:
                result = 'Esc'
            elif _ord == 10:
                result = '\n'
            elif _ord == 9:
                result = '\t'
            elif _ord < 32:
                result = curses.unctrl(char)
                result = result.decode()
                result = 'Ctrl-' + result[1]
            else:
                result = char

        elif isinstance(char, int):
            # char must be some kind of function key
            if char == curses.KEY_BACKSPACE:
                result = '\b'
            else:
                result = curses.keyname(char)
                result = result.decode()
                result = result[4] + result[5:].lower()
                # Remove parenthesis for function keys
                result.replace('(', '')
                result.replace(')', '')
        else:
            raise IOError('Can\'t handle input character type: {}.'
                          .format(str(type(char))))
        debug(result)
        return result

    def normal_mode(self):
        """We are in normal mode."""
        char = self.getchar()

        if char == 'Resize':
            self.create_windows()
        elif not self.session.interactionstack.isempty:
            self.interactive_mode(char)
        elif char == ':':
            self.command_win.prompt()
        elif char in self.session.key_mapping:
            action = self.session.key_mapping[char]
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


def publics(obj):
    """Return all object in __dir__ not starting with '_'"""
    return (name for name in dir(obj) if not name.startswith('_'))
