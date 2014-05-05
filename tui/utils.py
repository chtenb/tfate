"""This module contains several utility functions."""
import curses
from logging import debug

def getchar(stdscr):
    """Retrieve input character from user as a readable string."""
    while 1:
        try:
            char = stdscr.get_wch()
            break
        except curses.error:
            pass

    if isinstance(char, str):
        _ord = ord(char)

        # Replace special characters with a readable string
        if _ord == 27:
            result = 'Esc'
        elif _ord == 10:
            result = '\n'
        elif _ord == 9:
            result = '\t'
        elif _ord < 32:
            result = curses.unctrl(char)
            result = result.decode()
            result = 'Ctrl-' + result[1]
        else:
            result = char

    elif isinstance(char, int):
        # char must be some kind of function key
        if char == curses.KEY_BACKSPACE:
            result = '\b'
        else:
            result = curses.keyname(char)
            result = result.decode()
            result = result[4] + result[5:].lower()
            # Remove parenthesis for function keys
            result.replace('(', '')
            result.replace(')', '')
    else:
        raise IOError('Can\'t handle input character type: {}.'
                        .format(str(type(char))))
    debug(result)
    return result

def publics(obj):
    """Return all object in __dir__ not starting with '_'"""
    return (name for name in dir(obj) if not name.startswith('_'))
