import sys

sys.path.insert(0, '/home/chiel/Projects/protexted')

import text
from selection import Selection
import selectors
import operators
import curses
from curses import wrapper
from curses.textpad import Textbox


def main(stdscr):
    t = text.Text(sys.argv[1])
    curses.curs_set(0)
    selection = Selection()
    operation = None
    selection.add((0, 1))

    while 1:
        stdscr.move(0, 0)

        lower_bound = 0
        y,x = stdscr.getmaxyx()
        upper_bound = y * x
        doesnt_fit = False
        bounded_selection = selection.bound(lower_bound, upper_bound)
        bounded_partition = selection.partition(t).bound(lower_bound, upper_bound)
        for interval in bounded_partition:
            try:
                if interval in bounded_selection:
                    stdscr.addstr(t.interval_content(*interval), curses.A_REVERSE)
                else:
                    stdscr.addstr(t.interval_content(*interval))
            except Exception as e:
                doesnt_fit = True
                break

        if not doesnt_fit:
            stdscr.addstr("EOF", curses.A_BOLD)
            stdscr.addstr(str(selection), curses.A_BOLD)  # DEBUG
        stdscr.clrtobot()
        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('j'):
            selection = selectors.move_to_next_line(t, selection)
        elif key == ord('k'):
            selection = selectors.move_to_previous_line(t, selection)
        elif key == ord('l'):
            selection = selectors.move_to_next_char(t, selection)
        elif key == ord('h'):
            selection = selectors.move_to_previous_char(t, selection)
        elif key == ord('i'):
            insert_text = ""
            while 1:
                key2 = stdscr.getch()
                if key2 == 27:
                    if operation != None:
                        t.apply_operation(operation)
                        selection = operation.new_selection
                    break;
                else:
                    insert_text += chr(key2)
                    operation = operators.insert_before(t, selection, insert_text)

            #insert_text = get_input(stdscr)
            #if key2 == ord('a'):
                #operation = operators.insert_before(t, selection, insert_text)
            #elif key2 == ord('s'):
                #operation = operators.insert_around(t, selection, insert_text)
            #elif key2 == ord('d'):
                #operation = operators.insert_in_place(
                    #t, selection, insert_text)
            #elif key2 == ord('f'):
                #operation = operators.insert_after(t, selection, insert_text)
            #else:
                #continue

        elif key == ord(':'):
            command = get_input(stdscr)
            try:
                exec(command)
            except Exception as e:
                stdscr.addstr(str(e))
                stdscr.addstr("\nPress any key...")
                stdscr.refresh()
                stdscr.getch()


def get_input(stdscr):
    y, x = stdscr.getmaxyx()
    stdscr.addstr(y - 1, 0, ">>")
    stdscr.refresh()
    s = curses.newwin(1, x - 1, y - 1, 1)
    s.refresh()
    text_box = Textbox(s)
    text_box.edit()
    return text_box.gather()[:-1]

wrapper(main)
