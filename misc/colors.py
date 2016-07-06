"""This module is for messing with the terminal colors."""
import os
import sys
unicurses_path = os.path.dirname(os.path.abspath(__file__)) + '/../libs/unicurses'
sys.path.insert(0, unicurses_path)

import unicurses as curses

tui_path = os.path.dirname(os.path.abspath(__file__)) + '/../tui'
sys.path.insert(0, tui_path)

import terminal

def main(stdscr):
    """
    There are 256 colors.
    The other bits are used for additional attributes.

    Passing the number -1 as color falls back to
    the default background and foreground colors.
    The color pair 0 (mod 256) is fixed on (-1, -1).
    The colors 0 till 15 are the terminal palette colors.
    """
    COLORS = 16
    COLOR_PAIRS = 16

    # Print color support
    curses.addstr('can_change_color: {}\n'.format(curses.can_change_color()))
    curses.addstr('has_colors: {}\n'.format(curses.has_colors()))
    curses.addstr('COLORS: {}\n'.format(COLORS))
    curses.addstr('COLOR_PAIRS: {}\n'.format(COLOR_PAIRS))

    # Init color options
    curses.start_color()
    curses.use_default_colors()

    # Init color pairs
    for i in range(COLORS):
        curses.init_pair(i, i, 0)
        curses.init_pair(i + COLORS, i, 3)
        #curses.addstr(str(curses.color_pair(i)) + ', ')

    # Demonstrate color pairs
    curses.addstr('\ncolorpairs: \n')
    for i in range(COLORS):
        attribute = curses.color_pair(i)
        curses.addstr('color_pair: {}, attribute: {}\n'.format(i, attribute), attribute)

    # Demonstrate attributes
    curses.addstr('\nattributes: \n')
    for name in ['A_NORMAL',
                 'A_STANDOUT',
                 'A_UNDERLINE',
                 'A_REVERSE',
                 'A_BLINK',
                 'A_DIM',
                 'A_BOLD',
                 'A_PROTECT',
                 'A_INVIS',
                 'A_ALTCHARSET',
                 'A_CHARTEXT',
                 'A_TOP',
                 'A_LOW',
                 'A_VERTICAL',
                 'A_HORIZONTAL',
                 'A_LEFT',
                 'A_RIGHT',
                 ]:
        try:
            attribute = curses.__dict__[name]
            curses.addstr('name: {}, attribute: {}\n'.format(name, attribute), attribute)
        except KeyError:
            curses.addstr('{} is not supported\n'.format(name))


    curses.refresh()
    curses.getch()
    curses.endwin()

terminal.init()
main(terminal.stdscr)
