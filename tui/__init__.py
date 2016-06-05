"""
NOTE: first set active_ui, then call main.
"""

from time import sleep
from threading import Thread
from logging import debug, info, critical
import unicurses as curses

from fate import document, run
from fate.document import documentlist, Document

from . import terminal


# Frames per second
refresh_rate = 20


def start(filenames: list):
    """Initialize curses and start application."""
    terminal.init()

    try:
        from .textuserinterface import TextUserInterface

        Document.create_userinterface = TextUserInterface

        # Create all documents
        if not filenames:
            filenames = ['']
        for filename in filenames:
            Document(filename)

        # Activate first document
        documentlist[0].ui.activate()

        # The main loop of the userinterface.
        screen_thread = Thread(target=screen_loop)
        screen_thread.start()

        # The main loop of fate itself
        run()
    except BaseException as e:
        critical('Uncaught exception! Error message: {}'.format(e.args))
        if screen_thread.is_alive():
            info('Joining screen thread')
            document.activedocument = None
            screen_thread.join()
            curses.endwin()
        raise e
    else:
        if screen_thread.is_alive():
            info('Joining screen thread')
            document.activedocument = None
            screen_thread.join()
            curses.endwin()

    info('Fate thread terminated.')


def screen_loop():
    """Loop that refreshes screen when touched."""
    try:
        while document.activedocument != None:
            if document.activedocument.ui.touched:
                document.activedocument.ui.touched = False
                document.activedocument.ui.refresh()
            sleep(1 / refresh_rate)
    except BaseException as e:
        critical('Error in screen thread!')
        info('Ending curses')
        curses.endwin()
        raise e
    else:
        info('Ending curses')
        curses.endwin()

    info('Screen thread terminated.')
