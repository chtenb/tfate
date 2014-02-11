"""This module is for messing with the terminal colors."""
import curses

def main(stdscr):
    """
    There are 256 colors.
    The other bits are used for additional attributes.
    The number -1 falls back to the default background and foreground colors.
    The color pair 0 (mod 256) is fixed on (-1, -1).
    The colors 0 till 15 are the terminal palette colors.
    8 till 15 are the lighter variants of 0 till 7.
    """
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, 8)
    try:
        for i in range(0, 512):
            stdscr.addstr(str(i), curses.color_pair(i))
    except curses.ERR:
        # End of screen reached
        pass
    stdscr.getch()

curses.wrapper(main)
