import sys

sys.path.insert(0, '/home/chiel/Projects/protexted')

import text
from selection import Selection
from selectors import bound, partition
import selectors
import operators
import curses
from curses.textpad import Textbox


class UserInterface:
    def __init__(self):
        self.text = text.Text(sys.argv[1])
        self.selection = Selection()
        self.selection.add((0, 1))
        self.screen_start = 0

    def main(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        y, x = self.stdscr.getmaxyx()
        self.text_win = curses.newwin(y - 1, x, 0, 0)
        self.status_win = curses.newwin(1, x, y - 1, 0)
        while 1:
            self.draw_text_win()
            self.user_input()

    def user_input(self):
        key = self.stdscr.getch()
        if key == ord('j'):
            self.selection = selectors.move_to_next_line(self.selection, self.text)
        elif key == ord('k'):
            self.selection = selectors.move_to_previous_line(self.selection, self.text)
        elif key == ord('l'):
            self.selection = selectors.move_to_next_char(self.selection, self.text)
        elif key == ord('h'):
            self.selection = selectors.move_to_previous_char(self.selection, self.text)
        elif key == ord('i'):
            self.insert_mode(operators.insert_before)
        elif key == ord('c'):
            self.insert_mode(operators.insert_in_place)
        elif key == ord(':'):
            command = self.get_input(self.status_win)
            try:
                exec(command)
            except Exception as e:
                self.draw_status(str(e))
            self.status_win.getch()

    def insert_mode(self, operator):
        insert_text = ""
        operation = None
        while 1:
            key2 = self.stdscr.getch()
            if key2 == 27:
                if operation != None:
                    self.text.apply_operation(operation)
                    self.selection = operation.new_selection
                break;
            else:
                insert_text += chr(key2)
                operation = operator(self.text, self.selection, insert_text)
            self.draw_text_win(operation)

    def get_input(self, scr):
        y, x = scr.getmaxyx()
        scr.addstr(y - 1, 0, ">>")
        scr.refresh()
        text_box = Textbox(scr)
        text_box.edit()
        return text_box.gather()[:-1]

    def draw_text_win(self, operation=None):
        self.text_win.move(0, 0)

        lower_bound = 0
        y, x = self.text_win.getmaxyx()
        upper_bound = y * x
        bounded_selection = bound(self.selection, lower_bound, upper_bound)
        bounded_partition = bound(partition(self.selection, self.text), lower_bound, upper_bound)
        selection_index = 0
        try:
            for interval in bounded_partition:
                if interval in bounded_selection:
                    if operation == None:
                        self.text_win.addstr(self.text.interval_content(interval), curses.A_REVERSE)
                    else:
                        self.text_win.addstr(operation.new_content[selection_index], curses.A_REVERSE)
                    selection_index += 1
                else:
                    self.text_win.addstr(self.text.interval_content(interval))
            self.text_win.addstr("EOF", curses.A_BOLD)
            self.text_win.addstr(str(self.selection), curses.A_BOLD)  # DEBUG
        except:
            pass
        self.text_win.clrtobot()
        self.text_win.refresh()

    def draw_status(self, string):
        try:
            self.status_win.addstr(0, 0, string)
        except:
            pass
        self.status_win.clrtobot()
        self.status_win.refresh()

ui = UserInterface()
curses.wrapper(ui.main)
