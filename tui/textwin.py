"Module containing TextWin class."""
import curses
from .win import Win


class TextWin(Win):
    """Window containing the text"""

    def __init__(self, width, height, x, y, session):
        Win.__init__(self, width, height, x, y, session)

    def draw(self, pending_operation=None):
        """Draw the visible text in the text window."""
        self.win.move(0, 0)

        # Find a suitable starting position
        ymax, xmax = self.win.getmaxyx()
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

            self.win.addstr('EOF\n', curses.A_BOLD)
        except curses.error:
            # End of window reached
            pass

        self.win.clrtobot()
        self.win.refresh()

    def draw_operation_interval(self, interval, content):
        """Draw an interval which is operated upon."""
        content = content.replace('\n', '↵\n') or 'ε'
        self.win.addstr(content, curses.A_BOLD | curses.A_REVERSE)

    def draw_interval(self, interval, selected=False):
        """Draw a regular interval."""
        beg, end = interval
        if end - beg == 0:
            self.win.addstr('ε', curses.A_REVERSE)
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

                self.win.addstr(char, attribute)

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
