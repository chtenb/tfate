#!python
"""This module is for messing with input characters."""
import curses
import signal

def signal_handler(sig, frame):
    pass

# Intercept ctrl-c, ctrl-\ and ctrl-z
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGQUIT, signal_handler)
signal.signal(signal.SIGTSTP, signal_handler)

def main(stdscr):
    stdscr.keypad(1)

    c = curses.erasechar()
    stdscr.addstr('repr: {}, type: {}\n\n'.format(repr(c), type(c)))

    while 1:
        c = stdscr.get_wch()
        #c = stdscr.getch()
        if c == ord('q'):
            break

        if isinstance(c, int):
            try:
                char = chr(c)
            except ValueError:
                char = 'not in range'
            try:
                name = curses.keyname(c)
            except ValueError:
                name = 'not in range'
            stdscr.addstr('repr: {}, chr: {}, name: {}\n'.format(repr(c), char, name))
        else:
            try:
                nr = ord(c)
            except ValueError:
                nr = 'not in range'
            stdscr.addstr('repr: {}, ord: {}, type: {}\n'.format(repr(c), nr, type(c)))
curses.wrapper(main)
