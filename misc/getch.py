"""This module is for messing with input characters."""
import curses
import locale

def main(stdscr):
    stdscr.addstr('œ')
    stdscr.addstr(repr(curses.erasechar()))
    stdscr.addstr('\n')
    while 1:
        c = stdscr.get_wch()
        if isinstance(c, int):
            stdscr.addstr("{}: {}, {}\n".format(repr(c), chr(c), curses.keyname(c)))
        else:
            stdscr.addstr("{}: {}\n".format(repr(c), type(c)))
curses.wrapper(main)
