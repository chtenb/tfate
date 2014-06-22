import unicurses as curses
from .textuserinterface import TextUserInterface
from fate import session
from logging import debug, info
import os


# Lower the annoying delay for the escape character
# VIM also uses 25 ms
os.environ['ESCDELAY'] = '25'


def init_colors(stdscr):
    # Initialize color pairs from the terminal color palette
    # Pair 0 is the default, pairs 1-16 are the palette colors,
    # pairs 17-32 are palette colors with a different background.
    # We assume that color 8 has good contrast with other colors.

    global HAS_COLORS
    HAS_COLORS = curses.has_colors()
    #HAS_COLORS = False

    if HAS_COLORS:
        curses.start_color()
        curses.use_default_colors()

        global HAS_BACKGROUND_COLORS
        HAS_BACKGROUND_COLORS = True
        if HAS_BACKGROUND_COLORS:
            info('Terminal supports background colors.')
        else:
            info('Terminal does not support background colors.')

        global COLOR_PAIRS
        #COLOR_PAIRS = min(16, curses.COLORS)
        COLOR_PAIRS = 16
        info('Terminal supports {} colors. Using {} colorpairs.'
             .format(16, COLOR_PAIRS))

        for i in range(COLOR_PAIRS):
            curses.init_pair(i + 1, i, -1)
            try:
                curses.init_pair(i + 1 + COLOR_PAIRS, i, 8)
                curses.init_pair(i + 1 + COLOR_PAIRS + COLOR_PAIRS, i, 9)
            except:
                HAS_BACKGROUND_COLORS = False


def start(filenames):
    """Initialize curses and start application."""
    stdscr = curses.initscr()

    # Display settings
    curses.cbreak()
    curses.noecho()

    # Key input settings
    curses.raw()
    curses.keypad(stdscr, 1)

    # No cursor
    curses.curs_set(0)

    try:
        # Init colors
        init_colors(stdscr)

        # Create all interfaces
        for filename in filenames:
            ui = TextUserInterface(stdscr, filename)
        session.session_list[0].ui.activate()

        while 1:
            ui = next(s.ui for s in session.session_list if s.ui.active)
            ui.main()
    except:
        raise
    finally:
        curses.endwin()
