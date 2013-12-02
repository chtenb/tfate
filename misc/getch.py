import curses

def main(stdscr):
    while 1:
        c = stdscr.getch()
        stdscr.addstr(chr(c) + ": " + str(c) + "\n")
curses.wrapper(main)
