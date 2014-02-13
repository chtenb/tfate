"""This module contains the UserInterface class."""
from fate.session import Session
from fate import actors, selectors, operators, modes
from . import key_mapping
import user
import curses
import sys
from .textwin import TextWin
from .clipboardwin import ClipboardWin
from .actionwin import ActionWin
from .statuswin import StatusWin


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
        self.stdscr.refresh()

    def normal_mode(self):
        """We are in normal mode."""
        key = chr(self.stdscr.getch())

        if key == chr(curses.KEY_RESIZE):
            self.create_windows()
        elif key == ':':
            self.command_mode()
        elif key in self.action_keys:
            self.action_keys[key](self.session)
        elif key in self.ui_action_keys:
            self.ui_action_keys[key](self)

    def command_mode(self):
        """We are in command mode."""
        session = self.session
        scope = vars(session)
        scope.update({'self': session})
        scope.update({'selectors': selectors})
        scope.update({'operators': operators})
        scope.update({'actors': actors})
        command = self.status_win.prompt(':')
        try:
            result = eval(command, scope)
            if result != None:
                self.status_win.set_status(str(result))
                self.stdscr.getch()
        except Exception as e:
            self.status_win.draw_status(command + ' : ' + str(e))
            self.stdscr.getch()
        self.status_win.refresh()

    def insert_mode(self, operator_constructor):
        """We are in insert mode."""
        self.mode = 'OPERATION'
        self.status_win.refresh()
        insertions = ''
        deletions = 0
        while 1:
            # Apply the operator to provide a preview
            pending_operator = operator_constructor(insertions, deletions)
            pending_operator(self.session)

            self.text_win.refresh()
            key = self.stdscr.getch()
            if key == 27:
                break
            elif key == curses.KEY_BACKSPACE:
                if insertions:
                    insertions = insertions[:-1]
                else:
                    deletions += 1
            elif key == curses.KEY_DC:
                # Do something useful here?
                pass
            else:
                insertions += chr(key)

            # Undo the preview of the pending operator
            self.session.actiontree.hard_undo()

    def prompt(self, prompt_string='>'):
        """Prompt the user for an input string."""
        return self.status_win.prompt(prompt_string)

