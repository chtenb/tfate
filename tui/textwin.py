"Module containing TextWin class."""
from .window import Window, EndOfWin
from logging import info


class TextWin(Window):

    """Window containing the text"""

    def __init__(self, ui):
        Window.__init__(self, ui)
        self.offset = (0, 0)

    def draw(self):
        """Draw the visible text in the text window."""
        selection = self.document.selection
        text = self.document.text
        labeling = self.document.labeling

        # Find a suitable starting position
        length = len(text)
        #position = move_n_wrapped_lines_up(text, self.width,
                                           #max(0, selection[0][0]),
                                           #int(self.height / 2))
        position = self.offset


        # Find the places of all empty selected intervals
        empty_interval_positions = [beg for beg, end in selection if end - beg == 0 and
                                    beg >= position]

        # Compute the line number of the first line
        number_of_lines = text.count('\n', 0)
        number_width = len(str(number_of_lines))
        linenumber = text.count('\n', 0, position)
        numbercolor = self.create_attribute(color=2)
        self.draw_string(str(linenumber) + (number_width - len(str(linenumber)) + 1) * ' ',
                         numbercolor)

        # Draw every character
        while 1:
            try:
                if position >= length and not empty_interval_positions:
                    self.draw_line('EOF', self.create_attribute(bold=True), silent=False)
                    break

                # Draw possible empty selected interval at position
                if empty_interval_positions and empty_interval_positions[0] == position:
                    #self.draw_string('ε', self.create_attribute(reverse=True), silent=False)
                    self.draw_string('E', self.create_attribute(reverse=True, bold=True),
                                     silent=False)
                    del empty_interval_positions[0]
                    continue

                assert position < length

                reverse = False
                highlight = False
                color = 0
                char = text[position]
                drawchar = char

                if char == '\t':
                    drawchar = self.document.tabwidth * ' '

                # Apply reverse attribute when char is selected
                if selection.contains(position):
                    reverse = True
                    # display newline character explicitly when selected
                    if char == '\n':
                        #char = '↵\n'
                        drawchar = ' \n'

                # Apply highlight attribute when char is locked
                if (self.document.locked_selection != None
                        and self.document.locked_selection.contains(position)):
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

                # Draw line numbers
                if char == '\n':
                    linenumber += 1
                    self.draw_string(str(linenumber) + (number_width - len(str(linenumber)) + 1) * ' ', numbercolor)

            except EndOfWin:
                break

