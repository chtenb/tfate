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
from .promptwin import PromptWin
from .logwin import LogWin
from . import utils
from .terminal import stdscr

from logging import debug


class TextUserInterface(userinterface.UserInterface):

    """
    This class provides a user interface for interacting with a document object.
    """

    def __init__(self, doc):
        userinterface.UserInterface.__init__(self, doc)
        self.active = False
        self.touched = False

        self.document_win = DocumentWin(self)
        self.text_win = TextWin(self)
        self.log_win = LogWin(self)
        self.status_win = StatusWin(self)

        self.prompt_win = PromptWin(self)
        self.undo_win = UndoWin(self)
        self.clipboard_win = ClipboardWin(self)

        self.windows = [self.document_win, self.text_win, self.log_win,
                        self.clipboard_win, self.undo_win, self.status_win,
                        self.prompt_win]

        self.clipboard_win.enabled = False
        self.prompt_win.enabled = False
        self.undo_win.enabled = False

        self.update_windows()

    def update_windows(self):
        """Give all windows correct sizes and positions."""
        ymax, xmax = curses.getmaxyx(stdscr)

        # We draw the windows bottom up
        linenumber = ymax

        status_win_height = 1
        linenumber -= status_win_height
        self.status_win.reset(xmax, status_win_height, 0, linenumber)

        log_win_height = 1
        linenumber -= log_win_height
        self.log_win.reset(xmax, log_win_height, 0, linenumber)

        if self.undo_win.enabled:
            undo_win_height = 4
            linenumber -= undo_win_height
            self.undo_win.reset(xmax, undo_win_height, 0, linenumber)

        if self.clipboard_win.enabled:
            clipboard_win_height = 3
            linenumber -= clipboard_win_height
            self.clipboard_win.reset(xmax, clipboard_win_height, 0, linenumber)

        self.text_win.reset(xmax, linenumber - 1, 0, 1)
        self.document_win.reset(xmax, 1, 0, 0)

        self.prompt_win.reset(int(xmax / 2), 2, int(xmax / 2), 4)
        self.touch()

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
                self.update_windows()
                self.touch()
            else:
                return key

document.Document.default_userinterface = TextUserInterface
