"""This module contains the key mapping as a dictionary from chars to actions, named `key_mapping`."""
from fatecore import selectors, actions, operators

key_mapping = {
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
    'x': operators.delete,
}
