"""This module contains functions which act on the user interface. We shall call them ui actors."""
from fate import actors, selectors, operators
import re

def quit_session(ui):
    if not ui.session.saved:
        ui.status_win.set_status("Unsaved changes! Really quit? (y/n)")
        while 1:
            char = chr(ui.stdscr.getch())
            if char == 'y':
                exit()
            if char == 'n':
                break
    else:
        exit()


def local_find(ui):
    char = chr(ui.stdscr.getch())
    selectors.local_pattern_selector(re.escape(char))(ui.session)


def local_find_backwards(ui):
    char = chr(ui.stdscr.getch())
    selectors.local_pattern_selector(re.escape(char), reverse=True)(ui.session)


def search(ui):
    s = ui.session
    s.search_pattern = ui.prompt('/')
    selectors.global_pattern_selector(s.search_pattern)(s)


def search_current_content(ui):
    s = ui.session
    s.search_pattern = re.escape(s.content(s.selection)[-1])
    selectors.global_pattern_selector(s.search_pattern)(s)


def search_next(ui):
    s = ui.session
    if s.search_pattern:
        selectors.global_pattern_selector(s.search_pattern)(s)


def search_previous(ui):
    s = ui.session
    if s.search_pattern:
        selectors.global_pattern_selector(s.search_pattern, reverse=True)(s)


def open_line_after(ui):
    actors.open_line_after(ui.session)
    ui.insert_mode(operators.change_after)


def open_line_before(ui):
    actors.open_line_before(ui.session)
    ui.insert_mode(operators.change_after)

