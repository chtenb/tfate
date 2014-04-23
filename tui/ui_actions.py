"""
This module contains functions which act on the user interface.
We shall call them ui actors.
"""
from fate import actors, selectors, operators
import re
from .userinterface import UserInterface, ui_list


def quit_session(ui):
    if not ui.session.saved:
        ui.status_win.draw_status('Unsaved changes! Really quit? (y/n)')
        while 1:
            char = chr(ui.stdscr.getch())
            if char == 'y':
                exit()
            if char == 'n':
                break
    else:
        exit()


def open_session(ui):
    filename = ui.status_win.prompt('filename: ')
    ui = UserInterface(ui.stdscr, filename)
    ui.activate()

def next_session(ui):
    index = ui_list.index(ui)
    next_ui = ui_list[(index + 1) % len(ui_list)]
    next_ui.activate()


def local_find(ui):
    char = chr(ui.stdscr.getch())
    selectors.SelectLocalPattern(re.escape(char), ui.session)(ui.session)


def local_find_backwards(ui):
    char = chr(ui.stdscr.getch())
    selectors.SelectLocalPattern(re.escape(char), ui.session, reverse=True)(ui.session)


def search(ui):
    s = ui.session
    s.search_pattern = ui.prompt('/')
    try:
        selectors.SelectPattern(s.search_pattern, s)(s)
    except Exception as e:
        ui.status_win.draw_status(str(e))
        ui.stdscr.getch()


def search_current_content(ui):
    s = ui.session
    s.search_pattern = re.escape(s.content(s.selection)[-1])
    selectors.SelectPattern(s.search_pattern, s)(s)


def search_next(ui):
    s = ui.session
    if s.search_pattern:
        selectors.SelectPattern(s.search_pattern, s)(s)


def search_previous(ui):
    s = ui.session
    if s.search_pattern:
        selectors.SelectPattern(s.search_pattern, s, reverse=True)(s)
