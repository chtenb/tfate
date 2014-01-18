"""This module contains the UserInterface class."""
from fate.session import Session
from fate import actors, selectors, operators, modes
from . import key_mapping
import user
import curses
from curses.textpad import Textbox
import sys


class UserInterface:
    """This class provides a user interface for interacting with a session object."""
    def __init__(self):
        if len(sys.argv) > 1:
            self.session = Session(sys.argv[1])
        else:
            self.session = Session()
        self.session.read()
        self.session.search_pattern = ""
        self.mode = modes.SELECT_MODE

        # Load the right key mapping
        # User maps override the default maps
        self.action_keys = {}
        self.action_keys.update(key_mapping.action_keys)
        try:
            self.action_keys.update(user.action_keys)
        except AttributeError:
            pass

        self.ui_action_keys = {}
        self.ui_action_keys.update(key_mapping.ui_action_keys)
        try:
            self.ui_action_keys.update(user.ui_action_keys)
        except AttributeError:
            pass

    def main(self, stdscr):
        """Actually starts the user interface."""
        # Initialize color pairs from the terminal color palette
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i, i, -1)
        curses.init_pair(9, -1, 0)

        # Create curses windows
        self.stdscr = stdscr
        curses.curs_set(0)
        ymax, xmax = self.stdscr.getmaxyx()
        self.text_win = curses.newwin(ymax - 6, xmax, 0, 0)
        self.clipboard_win = curses.newwin(1, xmax, ymax - 6, 0)
        self.actiontree_win = curses.newwin(4, xmax, ymax - 5, 0)
        self.status_win = curses.newwin(1, xmax, ymax - 1, 0)
        self.stdscr.refresh()

        # Enter the main loop
        while 1:
            self.mode = self.session.selection_mode
            self.draw_text()
            self.draw_action_tree()
            self.draw_clipboard()
            self.normal_mode()

    def normal_mode(self):
        """We are in normal mode."""
        key = chr(self.stdscr.getch())

        if key in self.action_keys:
            self.action_keys[key](self.session)
        elif key in self.ui_action_keys:
            self.ui_action_keys[key](self)
        elif key == ':':
            self.command_mode()

    def command_mode(self):
        """We are in command mode."""
        session = self.session
        scope = vars(session)
        scope.update({'self': session})
        scope.update({'selectors': selectors})
        scope.update({'operators': operators})
        scope.update({'actors': actors})
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
        """We are in insert mode."""
        self.mode = 'OPERATION'
        insertions = ''
        deletions = 0
        while 1:
            pending_operator = operator_constructor(insertions, deletions)
            pending_operation = pending_operator(self.session, preview=True).sub_actions[0]
            self.draw_text(pending_operation)
            key = self.stdscr.getch()
            if key == 27:
                pending_operation.do()
                break
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

    def draw_text(self, pending_operation=None):
        """Draw the visible text in the text window."""
        self.text_win.move(0, 0)

        # Find a suitable starting position
        ymax, xmax = self.text_win.getmaxyx()
        selection = self.session.selection
        position = move_n_wrapped_lines_up(self.session.text, xmax,
                                           max(0, selection[0][0]), int(ymax / 2))

        try:
            # Find index of first selected interval that has to be drawn
            index = 0
            for index in range(len(selection)):
                if selection[index][1] > position:
                    break

            # Alternate between selected intervals and regular intervals
            while 1:
                if index < len(selection):
                    # interval is the next selected interval to be drawn
                    interval = selection[index]

                    if interval[0] <= position:
                        # Print selected interval
                        if pending_operation:
                            self.draw_operation_interval(interval,
                                                         pending_operation.new_content[index])
                        else:
                            self.draw_interval(interval, selected=True)
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
            # End of window reached
            pass

        try:
            self.set_status(self.session.filename
                            + ("*" if not self.session.saved else "")
                            + " | " + str(self.session.filetype)
                            + " | " + self.mode
                            + " | " + str(self.session.selection))
        except curses.error:
            # End of window reached
            pass

        self.text_win.clrtobot()
        self.text_win.refresh()

    def draw_operation_interval(self, interval, content):
        """Draw an interval which is operated upon."""
        content = content.replace('\n', '↵\n') or 'ε'
        self.text_win.addstr(content, curses.A_BOLD | curses.A_REVERSE)

    def draw_interval(self, interval, selected=False):
        """Draw a regular interval."""
        beg, end = interval
        if end - beg == 0:
            self.text_win.addstr('ε', curses.A_REVERSE)
        else:
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

    def set_status(self, string):
        """Set the content of the status window."""
        self.status_win.bkgd(' ', curses.color_pair(9))
        try:
            self.status_win.addstr(0, 0, string, curses.color_pair(9))
        except curses.error:
            # End of window reached
            pass
        self.status_win.clrtobot()
        self.status_win.refresh()

    def prompt(self, prompt_string='>'):
        """Prompt the user for an input string."""
        self.status_win.clear()
        ymax, xmax = self.stdscr.getmaxyx()
        self.status_win.addstr(0, 0, prompt_string)
        self.status_win.refresh()
        prompt_len = len(prompt_string)
        text_box_win = curses.newwin(1, xmax - prompt_len, ymax - 1, prompt_len)
        text_box_win.bkgd(' ', curses.color_pair(9))
        text_box = Textbox(text_box_win)
        text_box.edit()
        return text_box.gather()[:-1]

    def draw_action_tree(self):
        """Draw the current actiontree to the actiontree_win."""
        try:
            self.actiontree_win.addstr(0, 0, self.session.actiontree.dump())
        except curses.error:
            # End of window reached
            pass
        self.actiontree_win.clrtobot()
        self.actiontree_win.refresh()

    def draw_clipboard(self):
        """Draw the current clipboard to the clipboard_win."""
        try:
            self.clipboard_win.addstr(0, 0, self.session.clipboard.dump())
        except curses.error:
            # End of window reached
            pass
        self.clipboard_win.clrtobot()
        self.clipboard_win.refresh()


# TODO: needs refactoring
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
