"Module containing TextWin class."""
import curses
from .win import Win


class TextWin(Win):
    """Window containing the text"""

    def __init__(self, width, height, x, y, session):
        Win.__init__(self, width, height, x, y, session)

    def draw(self):
        """Draw the visible text in the text window."""
        selection = self.session.selection
        text = self.session.text
        labeling = self.session.labeling

        # Find a suitable starting position
        length = len(text)
        position = move_n_wrapped_lines_up(text, self.width,
                                           max(0, selection[0][0]),
                                           int(self.height / 2))

        # Find the places of all empty selected intervals
        empty_intervals = []
        for end, beg in selection:
            if end - beg == 0:
                empty_intervals.append(beg)

        # Draw every character
        while 1:
            if position >= length:
                self.draw_line('EOF', curses.A_BOLD)
                break

            # Draw possible empty selected interval at position
            if empty_intervals and empty_intervals[0] == position:
                self.win.addstr('ε', curses.A_REVERSE)
                empty_intervals.remove(empty_intervals[0])
                continue

            attribute = curses.A_NORMAL
            char = text[position]

            # Apply reverse attribute when char is selected
            if selection.contains(position):
                attribute |= curses.A_REVERSE
                # display newline character explicitly when selected
                if char == '\n':
                    char = '↵\n'

            # Apply color attribute if char is labeled
            if position in labeling:
                for i, label in enumerate(['string', 'number', 'keyword', 'comment']):
                    if labeling[position] == label:
                        attribute |= curses.color_pair(10 + i)

            try:
                self.win.addstr(char, attribute)
                position += 1
            except curses.error:
                # End of window reached
                break


def move_n_wrapped_lines_up(text, max_line_width, start, n):
    """Return position that is n lines above start."""
    position = text.rfind('\n', 0, start)
    if position <= 0:
        return 0
    while 1:
        previousline = text.rfind('\n', 0, position - 1)
        if previousline <= 0:
            return 0
        n -= int((position - previousline) / max_line_width) + 1
        if n <= 0:
            return position + 1
        position = previousline
