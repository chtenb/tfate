"""This module contains the UserInterface class."""
import unicurses as curses

#from fate.document import Document, documentlist
#from fate.userinterface import UserInterface
from fate import document, userinterface

from .documentwin import DocumentWin
from .textwin import TextWin
from .clipboardwin import ClipboardWin
from .undowin import UndoWin
from .statuswin import StatusWin
from .commandwin import CommandWin
from .logwin import LogWin
from . import utils, screen
from .terminal import stdscr

from logging import debug


class TextUserInterface(userinterface.UserInterface):

    """
    This class provides a user interface for interacting with a document object.
    """

    def __init__(self, document):
        userinterface.UserInterface.__init__(self, document)
        self.active = False
        self.touched = False

        self._create_windows()

    def _create_windows(self):
        """Create all curses windows."""
        ymax, xmax = curses.getmaxyx(stdscr)
        self.document_win = DocumentWin(xmax, 1, 0, 0, self)
        self.text_win = TextWin(xmax, ymax - 1 - 10 - 5 - 3 - 1, 0, 1, self)
        self.log_win = LogWin(xmax, 10, 0, ymax - 10 - 5 - 3 - 1, self)
        self.clipboard_win = ClipboardWin(xmax, 3, 0, ymax - 5 - 3 - 1, self)
        self.undo_win = UndoWin(xmax, 5, 0, ymax - 5 - 1, self)
        self.status_win = StatusWin(xmax, 1, 0, ymax - 1, self)

        self.command_win = CommandWin(int(xmax / 2), 2, int(xmax / 2), 4, self)

        self.windows = [self.document_win, self.text_win, self.log_win,
                        self.clipboard_win, self.undo_win, self.status_win,
                        self.command_win]

    def touch(self):
        """Tell the screen thread to update the screen."""
        self.touched = True

    def activate(self):
        """Activate the user interface."""
        document.activedocument = self.document
        self.touch()

    def deactivate(self):
        """Deactivate the user interface."""
        document.activedocument = None

    def refresh(self):
        """Refresh all windows."""
        for win in self.windows:
            win.refresh()

    def quit(self, document_arg):
        """Activate next document, if existent."""
        assert document_arg is self.document

        #index = document.documentlist.index(self.document)

        #debug(str(documentlist))
        #debug("self: " + str(self.document))
        #debug("index: " + str(index))
        #self.getkey()

        #if len(document.documentlist) == 1:
            #self.deactivate()
            #return

        #if index < len(document.documentlist) - 1:
            #next_document = document.documentlist[index + 1]
        #else:
            #next_document = document.documentlist[index - 1]

        ##debug("next: " + str(next_document))
        #next_document.ui.activate()

    #def getinput(self):
        #key = self.peekinput()
        #utils.getkey()
        #return key

    def _getuserinput(self):
        while 1:
            key = utils.getkey()
            # Intercept resize events
            if key == 'Resize':
                self._create_windows()
                self.touch()
            else:
                return key

    def command_mode(self):
        self.command_win.prompt()

    def prompt(self, prompt_string='>'):
        """Prompt the user for an input string."""
        return self.status_win.prompt(prompt_string)

    def notify(self, message):
        self.status_win.set_status(message)
        self.getkey()
        self.status_win.set_default_status()

document.Document.default_userinterface = TextUserInterface
