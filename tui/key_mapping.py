"""This module contains the key mapping as two dictionaries from chars to functions.
The first one, `actions`, maps chars to actions.
The second one, `ui_actions`, maps chars to ui actions,
i.e. functions which take an UserInterface object."""
from fate import selectors, actors, operators, modes, clipboard
from fate.session import Session
from . import ui_actions


action_keys = {
    'W': Session.write,
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
    'u': actors.undo,
    'U': actors.redo,
    'y': actors.copy,
    'Y': clipboard.clear,
    'p': clipboard.paste_after,
    'P': clipboard.paste_before,
    'x': actors.cut,
    chr(27): actors.escape,
    'd': operators.delete,
    'r': modes.reduce_mode,
    'e': modes.extend_mode,
}

ui_action_keys = {
    'Q': ui_actions.quit_session,
    'f': ui_actions.local_find,
    'F': ui_actions.local_find_backwards,
    '/': ui_actions.search,
    '*': ui_actions.search_current_content,
    'n': ui_actions.search_next,
    'N': ui_actions.search_previous,
    'i': lambda ui: ui.insert_mode(operators.change_before),
    'a': lambda ui: ui.insert_mode(operators.change_after),
    's': lambda ui: ui.insert_mode(operators.change_around),
    'c': lambda ui: ui.insert_mode(operators.change_in_place),
    'o': ui_actions.open_line_after,
    'O': ui_actions.open_line_before,
}

