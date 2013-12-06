"""This module contains the key mapping as two dictionaries from chars to functions. The first one, `actions`, maps chars to actions. The second one, `ui_actions`, maps chars to function which take an UserInterface object."""
from fatecore import selectors, actions, operators
from fatecore.session import Session
import re


actions = {
    'W': Session.write,
    'u': Session.undo,
    'U': Session.redo,
    'j': selectors.next_line,
    'k': selectors.previous_line,
    'J': selectors.next_full_line,
    'K': selectors.previous_full_line,
    'l': selectors.next_char,
    'h': selectors.previous_char,
    'w': selectors.next_word,
    'b': selectors.previous_word,
    '}': selectors.next_paragraph,
    '{': selectors.previous_paragraph,
    'm': selectors.join,
    'z': selectors.complement,
    'A': selectors.everything,
    'y': actions.copy,
    'p': actions.paste_after,
    'P': actions.paste_before,
    'r': actions.reduce_mode,
    'e': actions.extend_mode,
    chr(27): actions.escape,
    'x': operators.delete,
}


def quit_session(ui):
    if not ui.session.saved:
        ui.set_status("Unsaved changes! Really quit? (y/n)")
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
    ui.session.apply(selectors.local_pattern_selector(re.escape(char)))


def local_find_backwards(ui):
    char = chr(ui.stdscr.getch())
    ui.session.apply(selectors.local_pattern_selector(re.escape(char), reverse=True))


def search(ui):
    s = ui.session
    s.search_pattern = ui.prompt('/')
    s.apply(selectors.global_pattern_selector(s.search_pattern))


def search_current_content(ui):
    s = ui.session
    s.search_pattern = re.escape(s.content(s.selection)[-1])
    s.apply(selectors.global_pattern_selector(s.search_pattern))


def search_next(ui):
    s = ui.session
    if s.search_pattern:
        s.apply(selectors.global_pattern_selector(s.search_pattern))


def search_previous(ui):
    s = ui.session
    if s.search_pattern:
        s.apply(selectors.global_pattern_selector(s.search_pattern, reverse=True))


def open_line_after(ui):
    ui.session.apply(actions.open_line_after)
    ui.insert_mode(operators.change_after)


def open_line_before(ui):
    ui.session.apply(actions.open_line_before)
    ui.insert_mode(operators.change_after)

ui_actions = {
    'Q': quit_session,
    'f': local_find,
    'F': local_find_backwards,
    '/': search,
    '*': search_current_content,
    'n': search_next,
    'N': search_previous,
    'i': lambda ui: ui.insert_mode(operators.change_before),
    'a': lambda ui: ui.insert_mode(operators.change_after),
    's': lambda ui: ui.insert_mode(operators.change_around),
    'c': lambda ui: ui.insert_mode(operators.change_in_place),
    'o': open_line_after,
    'O': open_line_before,
}
