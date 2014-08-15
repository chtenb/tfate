#!python
"""This module is for messing with input characters."""
import curses


def key_info(key):
    try:
        _ord = ord(key)
    except:
        _ord = -1
    try:
        _chr = chr(key)
    except:
        _chr = -1
    try:
        unctrl = curses.unctrl(key)
    except:
        unctrl = 'no unctrl'
    try:
        name = curses.keyname(key)
    except:
        name = 'no name'

    return ('repr: {}, type: {}, ord: {}, chr: {}, unctrl: {}, name: {}\n'
            .format(repr(key), type(key), _ord, _chr, unctrl, name))


def getchar(stdscr):
    while 1:
        try:
            char = stdscr.get_wch()
            break
        except curses.error:
            pass

    stdscr.addstr(key_info(char))

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

    stdscr.addstr(key_info(result))
    return result


def main(stdscr):
    stdscr.keypad(1)
    curses.raw()

    for i in range(127):
        stdscr.addstr(repr(chr(i)))

    stdscr.addstr('\n\n')

    for i in range(127):
        stdscr.addstr(repr(curses.unctrl(chr(i))))

    stdscr.addstr('special characters: {}\n\n'.format('œă好'))

    while 1:
        c = getchar(stdscr)
        if c == 'q':
            break
curses.wrapper(main)
