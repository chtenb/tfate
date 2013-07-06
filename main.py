import sys

sys.path.insert(0, '/home/chiel/Projects/protexted')

import text
import selections
import curses
from curses.wrapper import wrapper
from curses.textpad import Textbox


def main(stdscr):
    t = text.Text(sys.argv[1])
    curses.curs_set(0)
    cursor_pos = 0

    while 1:
        stdscr.addstr(0, 0, t.get_interval(0, cursor_pos))
        stdscr.addstr(t.get_interval(cursor_pos, cursor_pos + 1), curses.A_REVERSE)
        stdscr.addstr(t.get_interval(cursor_pos + 1, len(t)))
        stdscr.addstr("EOF", curses.A_BOLD)
        stdscr.clrtobot()
        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('j'):
            cursor_pos = selections.next_line(t, cursor_pos)
        if key == ord('k'):
            cursor_pos = selections.previous_line(t, cursor_pos)
        if key == ord('h'):
            cursor_pos = max(cursor_pos - 1, 0)
        if key == ord('l'):
            cursor_pos = min(cursor_pos + 1, len(t))
        if key == ord('i'):
            insert_text = get_input(stdscr)
            t.set_interval(cursor_pos, cursor_pos, insert_text)
        if key == ord(':'):
            command = get_input(stdscr)
            try:
                exec(command)
            except Exception as e:
                stdscr.addstr(str(e))
                stdscr.addstr("\nPress any key...")
                stdscr.refresh()
                stdscr.getch()

def get_input(stdscr):
    y,x = stdscr.getmaxyx()
    stdscr.addstr(y - 1, 0, ">")
    stdscr.refresh()
    s = curses.newwin(1,x - 1,y - 1,1)
    s.refresh()
    text_box = Textbox(s)
    text_box.edit()
    return text_box.gather()

wrapper(main)
