from fate.session import sessionlist, Session
from logging import debug, info
from . import terminal

import unicurses as curses

def start(filenames):
    """Initialize curses and start application."""
    terminal.init()

    try:
        from .textuserinterface import TextUserInterface
        from . import screen

        Session.UserInterfaceClass = TextUserInterface
        # Create all interfaces
        for filename in filenames:
            Session(filename)
        # Activate first session
        sessionlist[0].ui.activate()

        #debug(str(session.session_list))
        #debug(session.session_list[0].filename)
        #debug(screen.active_ui)

        screen.main()
        #while 1:
            #ui = next(s.ui for s in session.session_list if s.ui.active)
    except:
        curses.endwin()
        raise
    else:
        curses.endwin()

