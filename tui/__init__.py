from fate.document import documentlist, Document
from logging import debug, info
from . import terminal

import unicurses as curses

def start(filenames):
    """Initialize curses and start application."""
    terminal.init()

    try:
        from .textuserinterface import TextUserInterface
        from . import screen

        Document.UserInterfaceClass = TextUserInterface
        # Create all interfaces
        for filename in filenames:
            Document(filename)
        # Activate first document
        documentlist[0].ui.activate()

        #debug(str(document.document_list))
        #debug(document.document_list[0].filename)
        #debug(screen.active_ui)

        screen.main()
        #while 1:
            #ui = next(s.ui for s in document.document_list if s.ui.active)
    except:
        curses.endwin()
        raise
    else:
        curses.endwin()

