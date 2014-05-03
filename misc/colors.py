"""This module is for messing with the terminal colors."""
import curses


def main(stdscr):
    """
    There are 256 colors.
    The other bits are used for additional attributes.

    Passing the number -1 as color falls back to
    the default background and foreground colors.
    The color pair 0 (mod 256) is fixed on (-1, -1).
    The colors 0 till 15 are the terminal palette colors.
    """

    # Print color support
    stdscr.addstr('can_change_color: {}\n'.format(curses.can_change_color()))
    stdscr.addstr('has_colors: {}\n'.format(curses.has_colors()))
    stdscr.addstr('COLORS: {}\n'.format(curses.COLORS))
    stdscr.addstr('COLOR_PAIRS: {}\n'.format(curses.COLOR_PAIRS))

    stdscr.getch()

    # Init color options
    curses.start_color()
    curses.use_default_colors()

    # Show color contents
    #stdscr.addstr('colors:')
    #for i in range(curses.COLORS):
        #stdscr.addstr('{}: {}, '.format(str(i), curses.color_content(i)))
    #for i in range(-1, 256):
        #stdscr.addstr(str(i), i)
    #stdscr.getch()
    #exit()


    # Init color pairs
    for i in range(curses.COLORS):
        curses.init_pair(i + 1, i, -1)
        curses.init_pair(i + 1 + curses.COLORS, i, 3)
        #stdscr.addstr(str(curses.color_pair(i)) + ', ')

    # Demonstrate color pairs
    stdscr.addstr('\ncolorpairs: ')
    for i in range(curses.COLORS):
        stdscr.addstr(str(i + 1), curses.color_pair(i + 1))
    for i in range(curses.COLORS):
        stdscr.addstr(str(curses.COLORS + i + 1), curses.A_REVERSE ^ curses.color_pair(i + 1))

    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
