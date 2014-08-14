"""
NOTE: first set active_ui, then call main.
"""

from time import sleep
from threading import Thread
from logging import info
from fate import document, run

refresh_rate = 20


def screen_loop():
    """Loop that refreshes screen when touched."""
    while document.activedocument != None:
        if document.activedocument.ui.touched:
            document.activedocument.ui.touched = False
            document.activedocument.ui.refresh()
        sleep(1 / refresh_rate)
    info('Shutting down screen thread.')


def main():
    """The main loop of the userinterface."""
    try:
        screen_thread = Thread(target=screen_loop)
        screen_thread.start()
        run()
    except:
        raise
    finally:
        document.activedocument = None
