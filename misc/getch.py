#!python
"""This module is for messing with input characters."""
import curses
import signal


def handle_ctrl_c(sig, frame):
    curses.unget_wch(3)


def handle_ctrl_z(sig, frame):
    curses.unget_wch(26)

# Intercept ctrl-c, ctrl-z
signal.signal(signal.SIGINT, handle_ctrl_c)
signal.signal(signal.SIGTSTP, handle_ctrl_z)

def key_info(char):
    try:
        _ord = ord(char)
    except:
        _ord = -1
    try:
        _chr = chr(char)
    except:
        _chr = -1
    try:
        bytestring = curses.unctrl(char)
    except:
        bytestring = b'-1'
    try:
        name = curses.keyname(char)
    except:
        name = 'no name'

    return ('repr: {}, type: {}, ord: {}, chr: {}, bytestring: {}, name: {}\n'
                .format(repr(char), type(char), _ord, _chr, bytestring, name))


def getkey(stdscr):
    char = -1
    while char == -1:
        char = stdscr.getch()
        stdscr.addstr(key_info(char))

        try:
            result = curses.keyname(char)
        except:
            result = char
        else:
            result = result.decode()

        return result

def getchar(stdscr):
    char = -1
    while char == -1:
        char = stdscr.get_wch()
        stdscr.addstr(key_info(char))

        if isinstance(char, int):
            try:
                result = curses.keyname(char)
            except:
                result = char
            else:
                result = result.decode()
        else:
            result = char

        return result

def main(stdscr):
    stdscr.keypad(1)

    while 1:
        #c = getkey(stdscr)
        c = getchar(stdscr)
        if c == 'q':
            break
        stdscr.addstr('result: {}\n'.format(str(c)))
curses.wrapper(main)
