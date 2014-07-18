"Module containing TextWin class."""
from .win import Win, EndOfWin
from logging import debug


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
        empty_intervals = [beg for beg, end in reversed(selection)
                           if end - beg == 0]

        # Compute the line number of the first line
        number_of_lines = text.count('\n', 0)
        number_width = len(str(number_of_lines))
        linenumber = text.count('\n', 0, position)
        numbercolor = self.create_attribute(color=2)
        self.draw_string(str(linenumber) + (number_width - len(str(linenumber)) + 1) * ' ', numbercolor)

        # Draw every character
        while 1:
            try:
                if position >= length and not empty_intervals:
                    self.draw_line('EOF', self.create_attribute(bold=True), silent=False)
                    break

                # Draw possible empty selected interval at position
                if empty_intervals and empty_intervals[0] == position:
                    #self.draw_string('ε', self.create_attribute(reverse=True), silent=False)
                    self.draw_string('E', self.create_attribute(reverse=True, bold=True), silent=False)
                    empty_intervals.remove(empty_intervals[0])
                    continue

                reverse = False
                highlight = False
                color = 0
                #debug(position)
                char = text[position]
                drawchar = char

                if char == '\t':
                    drawchar = self.session.tabwidth * ' '

                # Apply reverse attribute when char is selected
                if selection.contains(position):
                    reverse = True
                    # display newline character explicitly when selected
                    if char == '\n':
                        #char = '↵\n'
                        drawchar = ' \n'

                # Apply highlight attribute when char is locked
                if (self.session.locked_selection != None
                        and self.session.locked_selection.contains(position)):
                    highlight = True
                    # display newline character explicitly when locked
                    if char == '\n':
                        #char = '↵\n'
                        drawchar = ' \n'

                # Apply color attribute if char is labeled
                if position in labeling:
                    for i, label in enumerate(['string', 'number', 'keyword', 'comment']):
                        if labeling[position] == label:
                            color = 11 + i

                attribute = self.create_attribute(reverse=reverse, color=color, highlight=highlight)

                self.draw_string(drawchar, attribute, silent=False)
                position += 1

                if char == '\n':
                    linenumber += 1
                    self.draw_string(str(linenumber) + (number_width - len(str(linenumber)) + 1) * ' ', numbercolor)

            except EndOfWin:
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
