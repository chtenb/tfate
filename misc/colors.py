import curses

def main(stdscr):
    curses.use_default_colors()
    for i in range(0,7):
        stdscr.addstr("Hello", curses.color_pair(i))
    stdscr.getch()

curses.wrapper(main)
