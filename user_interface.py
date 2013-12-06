from fatecore import session, selectors, operators, actions, modes
from fatecore.selection import Selection
import key_mapping
import curses
from curses.textpad import Textbox
import sys
import re
import logging


class UserInterface:
    def __init__(self):
        if len(sys.argv) > 1:
            self.session = session.Session(sys.argv[1])
        else:
            self.session = session.Session()
        self.session.read()
        self.session.searchPattern = ""

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
            self.mode = self.session.selection_mode
            self.draw_text()
            self.selection_mode()

    def selection_mode(self):
        key = chr(self.stdscr.getch())
        s = self.session

        if key in key_mapping.actions:
            s.apply(key_mapping.actions[key])
        elif key in key_mapping.ui_actions:
            key_mapping.ui_actions[key](self)
        elif key == ':':
            scope = vars(s)
            for name in vars(session.Session).keys():
                scope.update({name: eval('s.' + name)})
            scope.update({'self': s})
            scope.update({'selectors': selectors})
            scope.update({'operators': operators})
            scope.update({'actions': actions})
            command = self.prompt(':')
            try:
                result = eval(command, scope)
                if result != None:
                    self.set_status(str(result))
                    self.stdscr.getch()
            except Exception as e:
                self.set_status(command + ' : ' + str(e))
                self.stdscr.getch()
            self.status_win.clear()

    def insert_mode(self, operator_constructor):
        self.mode = 'OPERATION'
        insertions = ''
        deletions = 0
        while 1:
            pending_operator = operator_constructor(insertions, deletions)
            self.draw_text(pending_operator)
            key = self.stdscr.getch()
            if key == 27:
                self.session.apply(pending_operator)
                break;
            elif key == curses.KEY_BACKSPACE:
                if insertions:
                    insertions = insertions[:-1]
                else:
                    deletions += 1
            elif key == curses.KEY_DC:
                # Do something useful here?
                pass
            else:
                insertions += chr(key)

    def draw_operation_interval(self, interval, content):
        content = content.replace('\n', '↵\n') or 'ε'
        self.text_win.addstr(content, curses.A_BOLD | curses.A_REVERSE)

    def draw_selection_interval(self, interval):
        beg, end = interval
        if end - beg > 0:
            self.draw_interval(interval, selected=True)
        else:
            self.text_win.addstr('ε', curses.A_REVERSE)

    def draw_interval(self, interval, selected=False):
        beg, end = interval
        for position in range(beg, end):
            # Print next character of the interval
            attribute = curses.A_NORMAL
            char = self.session.text[position]

            # Apply attribute when char is selected
            if selected:
                attribute |= curses.A_REVERSE
                # Display newline character explicitly when selected
                if char == '\n':
                    char = '↵\n'

            # Apply attribute if char is labeled
            if position in self.session.labeling:
                for i, label in enumerate(['string', 'number', 'keyword', 'comment']):
                    if self.session.labeling[position] == label:
                        attribute |= curses.color_pair(i + 1)

            self.text_win.addstr(char, attribute)

    def draw_text(self, pending_operator=None):
        self.text_win.move(0, 0)

        # Find a suitable starting position
        y, x = self.text_win.getmaxyx()
        selection = self.session.selection
        position = move_n_wrapped_lines_up(self.session.text, x, max(0, selection[0][0]), int(y / 2))

        try:
            # Find index of first selected interval that has to be drawn
            for index in range(len(selection)):
                if selection[index][1] > position:
                    break

            # Alternate between selected intervals and regular intervals
            while 1:
                if index < len(selection):
                    interval = selection[index]  # interval is the next selected interval to be drawn

                    if interval[0] <= position:
                        # Print selected interval
                        if pending_operator:
                            self.draw_operation_interval(interval, pending_operator(self.session, preview=True).new_content[index])
                        else:
                            self.draw_selection_interval(interval)
                        position = interval[1]
                        index += 1
                    else:
                        # Print regular interval
                        self.draw_interval((position, interval[0]))
                        position = interval[0]
                else:
                    self.draw_interval((position, len(self.session.text)))
                    position = len(self.session.text)

                if position >= len(self.session.text):
                    break

            self.text_win.addstr('EOF\n', curses.A_BOLD)
        except curses.error:
            # End of screen reached
            pass

        try:
            self.set_status(self.session.filename +
                           ("*" if not self.session.saved else "") + " | " + str(self.session.filetype)
                            + " | " + self.mode + " | " + str(self.session.selection))
        except curses.error:
            # End of screen reached
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
    position = text.rfind('\n', 0, start)
    if position == -1:
        return 0
    while 1:
        next = text.rfind('\n', 0, position - 1)
        if next == -1:
            return 0
        n -= int((position - next) / wrap) + 1
        if n <= 0:
            return position + 1
        position = next
