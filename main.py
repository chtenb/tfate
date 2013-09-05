import sys
from protexted import session
from protexted import selectors, operators
from protexted.selection import Selection
import curses
from curses.textpad import Textbox
import re


class UserInterface:
    def __init__(self):
        self.session = session.Session(sys.argv[1])
        self.session.read()

    def main(self, stdscr):
        # Initialize color pairs from the terminal color palette
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i, i, -1);
        curses.init_pair(9, -1, 0);

        # Create curses windows
        self.stdscr = stdscr
        curses.curs_set(0)
        y, x = self.stdscr.getmaxyx()
        self.text_win = curses.newwin(y - 1, x, 0, 0)
        self.status_win = curses.newwin(1, x, y - 1, 0)
        self.stdscr.refresh()

        # Enter the main loop
        while 1:
            modes = []
            if self.session.extend_mode:
                modes.append('EXTEND')
            if self.session.reduce_mode:
                modes.append('REDUCE')
            self.set_status(' '.join(modes))
            self.draw_text()
            self.selection_mode()


    def selection_mode(self):
        key = self.stdscr.getch()
        if key == ord('j'):
            self.session.select(selectors.next_line)
        elif key == ord('k'):
            self.session.select(selectors.previous_line)
        elif key == ord('l'):
            self.session.select(selectors.next_char)
        elif key == ord('h'):
            self.session.select(selectors.previous_char)
        elif key == ord('w'):
            self.session.select(selectors.next_word)
        elif key == ord('b'):
            self.session.select(selectors.previous_word)
        elif key == ord('}'):
            self.session.select(selectors.next_paragraph)
        elif key == ord('{'):
            self.session.select(selectors.previous_paragraph)
        elif key == 27:
            self.session.select(selectors.single_character)
        elif key == ord('z'):
            self.session.select(selectors.complement)
        elif key == ord('f'):
            char = chr(self.stdscr.getch())
            self.session.select(selectors.pattern_selector(re.escape(char)))
        elif key == ord('/'):
            pattern = self.prompt('/')
            self.session.select(selectors.pattern_selector(pattern))
        elif key == ord('i'):
            self.insert_mode(operators.insert_before)
        elif key == ord('a'):
            self.insert_mode(operators.insert_after)
        elif key == ord('s'):
            self.insert_mode(operators.insert_around)
        elif key == ord('c'):
            self.insert_mode(operators.insert_in_place)
        elif key == ord('x'):
            operation = operators.delete(self.session.selection)
            self.session.apply(operation)
        elif key == ord('r'):
            self.session.reduce_mode = not self.session.reduce_mode
        elif key == ord('e'):
            self.session.extend_mode = not self.session.extend_mode
        elif key == ord('u'):
            self.session.undo()
        elif key == ord(':'):
            scope = vars(self.session)
            for name in vars(session.Session).keys():
                scope.update({name: eval('self.session.' + name)})
            command = self.prompt(':')
            try:
                print(eval(command, scope))
            except Exception as e:
                self.set_status(command + ' : ' + str(e))
                self.stdscr.getch()

    def insert_mode(self, operator):
        self.set_status('OPERATION')
        insert_text = ''
        while 1:
            operation = operator(self.session, self.session.selection, insert_text)
            self.draw_text(operation)
            key = self.stdscr.getch()
            if key == 27:
                if operation != None:
                    self.session.apply(operation)
                break;
            elif key == curses.KEY_BACKSPACE:
                if len(insert_text) > 0:
                    insert_text = insert_text[:-1]
            else:
                insert_text += chr(key)

    def draw_text(self, pending_operation=None):
        self.text_win.move(0, 0)
        # Find a suitable starting position
        y, x = self.text_win.getmaxyx()
        if self.session.selection:
            position = move_n_wrapped_lines_up(self.session.text, x, self.session.selection[0][0], int(y / 2))
        else:
            position = 0
        try:
            while position < len(self.session.text):
                if pending_operation:
                    # Print preview of operation if existent at current position
                    interval = pending_operation.old_selection.contains(position)
                    if interval:
                        index = pending_operation.old_selection.index(interval)
                        self.text_win.addstr(pending_operation.new_content[index], curses.A_BOLD | curses.A_REVERSE)
                        position += interval[1] - interval[0]
                        continue

                # Print next character of the text
                attribute = curses.A_NORMAL
                char = self.session.text[position]

                # Apply attribute when char is selected
                if self.session.selection.contains(position):
                    attribute |= curses.A_REVERSE
                    # Display newline character explicitly when selected
                    if char == '\n':
                        char = '↵\n'

                # Apply attribute when char is labeled
                if position in self.session.labeling:
                    for i, label in enumerate(['string', 'number', 'keyword', 'comment']):
                        if self.session.labeling[position] == label:
                            attribute |= curses.color_pair(i + 1)

                self.text_win.addstr(char, attribute)
                position += 1

            self.text_win.addstr('\nEOF', curses.A_BOLD)
            self.text_win.addstr(str(self.session.selection), curses.A_BOLD)  # DEBUG
            self.text_win.addstr(str(self.session.filetype), curses.A_BOLD)  # DEBUG
        except curses.error:
            pass

        self.text_win.clrtobot()
        self.text_win.refresh()

    def set_status(self, string):
        self.status_win.bkgd(' ', curses.color_pair(9))
        try:
            self.status_win.addstr(0, 0, string, curses.color_pair(9))
        except:
            pass
        self.status_win.clrtobot()
        self.status_win.refresh()

    def prompt(self, prompt_string='>'):
        self.status_win.clear()
        y, x = self.stdscr.getmaxyx()
        self.status_win.addstr(0, 0, prompt_string)
        self.status_win.refresh()
        l = len(prompt_string)
        text_box_win = curses.newwin(1, x - l, y - 1, l)
        text_box_win.bkgd(' ', curses.color_pair(9))
        text_box = Textbox(text_box_win)
        text_box.edit()
        return text_box.gather()[:-1]

def move_n_wrapped_lines_up(text, wrap, start, n):
    import math
    position = text.rfind('\n', 0, start)
    if position == -1:
        return 0
    while 1:
        next = text.rfind('\n', 0, position - 1)
        if next == -1:
            return 0
        n -= math.ceil((position - next) / wrap)
        if n <= 0:
            return position + 1
        position = next

ui = UserInterface()
curses.wrapper(ui.main)
