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
    'i': operators.change_before,
    'a': operators.change_after,
    's': operators.change_around,
    'c': operators.change_in_place,
    'o': actors.open_line_after,
    'O': actors.open_line_before,
}

ui_action_keys = {
    'Q': ui_actions.quit_session,
    'f': ui_actions.local_find,
    'F': ui_actions.local_find_backwards,
    '/': ui_actions.search,
    '*': ui_actions.search_current_content,
    'n': ui_actions.search_next,
    'N': ui_actions.search_previous,
}

def print_key_mapping():
    """Prints the keys with their explanation."""
    def print_key(key, action):
        print(key + ': ' + action.__docs__)

    for key, action in action_keys.items():
        print_key(key, action)
    for key, action in ui_action_keys.items():
        print_key(key, action)

