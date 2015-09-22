"""This module contains several utility functions."""
import unicurses as curses
from logging import debug

def getkey():
    """Retrieve input character from user as a readable string."""
    key = curses.getch()
    #debug(key)
    return key_to_string(key)

def peekkey():
    key = curses.getch()
    curses.ungetch(key)
    #debug(key)
    return key_to_string(key)


def key_to_string(key):
    """Replace special characters with a readable string"""
    if key == 27:
        result = 'esc'
    elif key == 10 or key == 13:
        result = '\n'
    elif key == 9:
        result = '\t'
    elif key == 8 or key == curses.KEY_BACKSPACE:
        result = '\b'
    elif key == 330 or key == curses.KEY_DC:
        result = 'del'
    elif key < 32:
        result = curses.unctrl(key)
        result = result.decode()
        result = 'ctrl-' + result[1].lower()
    elif key < 256:
        result = chr(key)
    else:
        # key must be some kind of function key
        try:
            result = curses.keyname(key)
        except:
            raise IOError('Can\'t handle input character type: {}.'
                            .format(str(type(key))))
        else:
            try:
                result = result.decode()
            except AttributeError:
                debug('Cant decode ' + repr(result))
            result = result[4:].lower()
            # Remove parenthesis for function keys
            result.replace('(', '')
            result.replace(')', '')
    #debug(result)
    return result
