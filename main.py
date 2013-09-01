import sys
from protexted import session
from protexted import selectors, operators
from protexted.selection import Selection
from protexted import current
import curses
from curses.textpad import Textbox


class UserInterface:
    def __init__(self):
        current.session = session.Session(sys.argv[1])
        current.session.read()
        current.session.selection = Selection()
        current.session.selection.add((0, 1))
        self.reduce_mode = False
        self.extend_mode = False

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
            if self.extend_mode:
                modes.append("EXTEND")
            if self.reduce_mode:
                modes.append("REDUCE")
            self.set_status(" ".join(modes))
            self.draw_text()
            self.selection_mode()

    def select(self, selector):
        if self.reduce_mode or self.extend_mode:
            if self.reduce_mode:
                current.session.selection = current.session.selection.reduce(selector, current.session.text)
            if self.extend_mode:
                current.session.selection = current.session.selection.extend(selector, current.session.text)
        else:
            current.session.selection = selector(current.session.selection)

    def selection_mode(self):
        key = self.stdscr.getch()
        if key == ord('j'):
            self.select(selectors.move_to_next_line)
        elif key == ord('k'):
            self.select(selectors.move_to_previous_line)
        elif key == ord('l'):
            self.select(selectors.next_char)
        elif key == ord('h'):
            self.select(selectors.previous_char)
        elif key == ord('w'):
            self.select(selectors.next_word)
        elif key == ord('b'):
            self.select(selectors.previous_word)
        elif key == ord('g'):
            self.select(selectors.next_group)
        elif key == 27:
            self.select(selectors.single_character)
        elif key == ord('z'):
            self.select(selectors.invert)
        elif key == ord('i'):
            self.operation_mode(operators.insert_before)
        elif key == ord('a'):
            self.operation_mode(operators.insert_after)
        elif key == ord('s'):
            self.operation_mode(operators.insert_around)
        elif key == ord('c'):
            self.operation_mode(operators.insert_in_place)
        elif key == ord('r'):
            self.reduce_mode = not self.reduce_mode
        elif key == ord('e'):
            self.extend_mode = not self.extend_mode
        elif key == ord('u'):
            current.session.undo()
        elif key == ord(':'):
            scope = vars(current.session)
            for name in vars(session.Session).keys():
                scope.update({name: eval('current.session.' + name)})
            scope.update({'current': current})
            scope.update({'selectors': selectors})
            command = self.prompt(":")
            try:
                exec(command, scope)
            except Exception as e:
                self.set_status(command + " : " + str(e))
                self.stdscr.getch()

    def operation_mode(self, operator):
        self.set_status("OPERATION")
        insert_text = ""
        while 1:
            operation = operator(current.session, current.session.selection, insert_text)
            self.draw_text(operation)
            self.set_status("Hi")
            key = self.stdscr.getch()
            if key == 27:
                if operation != None:
                    current.session.apply(operation)
                    current.session.selection = operation.new_selection
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
        position = move_n_wrapped_lines_up(current.session.text, x, current.session.selection[0][0], int(y / 2))
        try:
            while position < len(current.session.text):
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
                char = current.session.text[position]

                # Apply attribute when char is selected
                if current.session.selection.contains(position):
                    attribute |= curses.A_REVERSE
                    # Display newline character explicitly when selected
                    if char == '\n':
                        char = '↵\n'

                # Apply attribute when char is labeled
                if position in current.session.labeling:
                    for i, label in enumerate(['string', 'number', 'keyword', 'comment']):
                        if current.session.labeling[position] == label:
                            attribute |= curses.color_pair(i + 1)

                self.text_win.addstr(char, attribute)
                position += 1

            self.text_win.addstr("\nEOF", curses.A_BOLD)
            self.text_win.addstr(str(current.session.selection), curses.A_BOLD)  # DEBUG
            self.text_win.addstr(str(current.session.filetype), curses.A_BOLD)  # DEBUG
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

    def prompt(self, prompt_string=">"):
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
