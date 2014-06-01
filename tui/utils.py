"""This module contains several utility functions."""
import unicurses as curses
from logging import debug

def getchar(stdscr):
    """Retrieve input character from user as a readable string."""
    while 1:
        try:
            char = curses.getch()
            break
        except:
            pass

    # Replace special characters with a readable string
    if char == 27:
        result = 'Esc'
    elif char == 10:
        result = '\n'
    elif char == 9:
        result = '\t'
    elif char == curses.KEY_BACKSPACE:
        result = '\b'
    elif char < 32:
        result = curses.unctrl(char)
        result = result.decode()
        result = 'Ctrl-' + result[1]
    elif char < 256:
        result = chr(char)
    else:
        # char must be some kind of function key
        try:
            result = curses.keyname(char)
        except:
            raise IOError('Can\'t handle input character type: {}.'
                            .format(str(type(char))))
        else:
            result = result.decode()
            result = result[4] + result[5:].lower()
            # Remove parenthesis for function keys
            result.replace('(', '')
            result.replace(')', '')
    debug(result)
    return result
