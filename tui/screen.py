"""
NOTE: first set active_ui, then call main.
"""

from time import sleep
from threading import Thread
from logging import info

active_ui = None
refresh_rate = 20


def screen_loop():
    """Loop that refreshes screen when touched."""
    while active_ui != None:
        if active_ui.touched:
            active_ui.touched = False
            active_ui.refresh()
        sleep(1 / refresh_rate)
    info('Shutting down screen thread.')


def main():
    """The main loop of the userinterface."""
    global active_ui

    try:
        screen_thread = Thread(target=screen_loop)
        screen_thread.start()

        while active_ui != None:
            active_ui.touch()
            char = active_ui.getchar()

            if char in active_ui.session.keymap:
                action = active_ui.session.keymap[char]
                while callable(action):
                    action = action(active_ui.session)
    except:
        raise
    finally:
        active_ui = None
