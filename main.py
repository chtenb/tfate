import sys
from protexted import session
from protexted import selectors, operators
from protexted.selection import Selection
import curses
from curses.textpad import Textbox


class UserInterface:
    def __init__(self):
        session.current = session.Session(sys.argv[1])
        session.current.read()
        session.current.selection = Selection()
        session.current.selection.add((0, 1))

    def main(self, stdscr):
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i, i, curses.COLOR_BLACK)
            #stdscr.addstr("Foo", curses.color_pair(i))

        self.stdscr = stdscr
        curses.curs_set(0)
        y, x = self.stdscr.getmaxyx()
        self.text_win = curses.newwin(y - 1, x, 0, 0)
        self.status_win = curses.newwin(1, x, y - 1, 0)
        self.stdscr.refresh()
        while 1:
            self.draw_text_win()
            self.normal_mode()

    def normal_mode(self):
        key = self.stdscr.getch()
        if key == ord('j'):
            session.current.selection = selectors.move_to_next_line(session.current.selection)
        elif key == ord('k'):
            session.current.selection = selectors.move_to_previous_line(session.current.selection)
        elif key == ord('l'):
            session.current.selection = selectors.move_to_next_char(session.current.selection)
        elif key == ord('h'):
            session.current.selection = selectors.move_to_previous_char(session.current.selection)
        elif key == ord('i'):
            self.insert_mode(operators.insert_before)
        elif key == ord('c'):
            self.insert_mode(operators.insert_in_place)
        elif key == ord(':'):
            scope = {'selectors': selectors, 'operators': operators, 'session.current': session.current}
            command = self.prompt(":")
            try:
                exec(command, scope)
            except Exception as e:
                self.set_status(command + " : " + str(e))

    def insert_mode(self, operator):
        insert_text = ""
        operation = None
        while 1:
            key2 = self.stdscr.getch()
            if key2 == 27:
                if operation != None:
                    session.current.apply(operation)
                    session.current.selection = operation.new_selection
                break;
            else:
                insert_text += chr(key2)
                operation = operator(session.current, session.current.selection, insert_text)
            self.draw_text_win(operation)

    def prompt(self, prompt_string=">"):
        self.status_win.clear()
        y, x = self.stdscr.getmaxyx()
        self.status_win.addstr(0, 0, prompt_string)
        self.status_win.refresh()
        l = len(prompt_string)
        text_box_win = curses.newwin(1, x - l, y - 1, l)
        text_box = Textbox(text_box_win)
        text_box.edit()
        return text_box.gather()[:-1]

    def draw_text_win(self, pending_operation=None):
        #TODO rewrite this method
        self.text_win.move(0, 0)

        lower_bound = 0
        y, x = self.text_win.getmaxyx()
        upper_bound = y * x
        bounded_selection = selectors.bound(session.current.selection, lower_bound, upper_bound)
        bounded_partition = selectors.bound(selectors.partition(session.current.selection), lower_bound, upper_bound)
        selection_index = 0
        try:
            for interval in bounded_partition:
                if interval in bounded_selection:
                    if pending_operation == None:
                        self.text_win.addstr(session.current.text.get(interval), curses.color_pair(0) | curses.A_REVERSE)
                    else:
                        self.text_win.addstr(pending_operation.new_content[selection_index], curses.color_pair(1) | curses.A_REVERSE)
                    selection_index += 1
                else:
                    self.text_win.addstr(session.current.text.get(interval))
            self.text_win.addstr("EOF", curses.A_BOLD)
            self.text_win.addstr(str(session.current.selection), curses.A_BOLD)  # DEBUG
        except:
            pass
        self.text_win.clrtobot()
        self.text_win.refresh()

    def set_status(self, string):
        try:
            self.status_win.addstr(0, 0, string)
        except:
            pass
        self.status_win.clrtobot()
        self.status_win.refresh()

ui = UserInterface()
curses.wrapper(ui.main)
