"Module containing TextWin class."""
from .window import Window, EndOfWin
from logging import info


class TextWin(Window):

    """Window containing the text"""

    def __init__(self, ui):
        Window.__init__(self, ui)
        self.offset = 0

    def draw(self):
        """Draw the visible text in the text window."""
        # Compute the line number of the first line
        #number_of_lines = text.count('\n', 0) + 1
        #number_width = len(str(number_of_lines))
        #linenumber = text.count('\n', 0, position) + 1
        #numbercolor = self.create_attribute(color=2)
        #self.draw_string(str(linenumber) + (number_width - len(str(linenumber)) + 1) * ' ',
                         #numbercolor)

        textview = self.doc.view.text
        length = len(textview)
        highlightingview = self.doc.view.highlighting
        selectionview = self.doc.view.selection
        # Find the places of all empty selected intervals
        empty_interval_positions = [beg for beg, end in selectionview if end - beg == 0]

        try:
            for pos, char in enumerate(textview):
                # Draw possible empty selected interval at position
                if empty_interval_positions and empty_interval_positions[0] == pos:
                    try:
                        self.draw_string('ε', self.create_attribute(reverse=True), silent=False)
                    except UnicodeEncodeError:
                        self.draw_string('|', self.create_attribute(reverse=True), silent=False)
                    del empty_interval_positions[0]

                # Apply reverse attribute when char is selected
                reverse = False
                if selectionview.contains(pos):
                    reverse = True
                    # display newline character explicitly when selected
                    if char == '\n':
                        # char = '↵\n'
                        char = ' \n'
                        #drawchar = ' \n'

                # Apply color attribute if char is labeled
                alt_background = False
                if highlightingview[pos] == 'error':
                    alt_background = True
                elif highlightingview[pos] == 'warning':
                    alt_background = True

                color = 0
                for i, label in enumerate(['string', 'number', 'keyword', 'comment']):
                    if highlightingview[pos] == label:
                        color = 11 + i

                attribute = self.create_attribute(reverse=reverse, color=color,
                            highlight=False, alt_background=alt_background)
                self.draw_string(char, attribute, silent=False)

            # If we come here, the entire textview fits on the screen
            # Draw possible remaining empty interval
            if empty_interval_positions:
                try:
                    self.draw_string('ε', self.create_attribute(reverse=True), silent=False)
                except UnicodeEncodeError:
                    self.draw_string('|', self.create_attribute(reverse=True), silent=False)
            # Draw EOF character
            if not empty_interval_positions:
                self.draw_line('EOF', self.create_attribute(bold=True), silent=False)
        except EndOfWin:
            pass


        return

        selection = self.doc.selection
        text = self.doc.text
        labeling = self.doc.labeling

        # Find the places of all empty selected intervals
        empty_interval_positions = [beg for beg, end in selection if end - beg == 0 and
                                    beg >= position]

        # Draw every character
        while 1:
            try:
                if position >= length and not empty_interval_positions:
                    self.draw_line('EOF', self.create_attribute(bold=True), silent=False)
                    break

                # Draw possible empty selected interval at position
                if empty_interval_positions and empty_interval_positions[0] == position:
                    self.draw_string('ε', self.create_attribute(reverse=True), silent=False)
                    #self.draw_string('E', self.create_attribute(reverse=True, bold=True),
                                     #silent=False)
                    del empty_interval_positions[0]
                    continue

                assert position < length

                reverse = False
                highlight = False
                alt_background = False
                color = 0
                char = text[position]
                drawchar = char

                if char == '\t':
                    drawchar = self.doc.tabwidth * ' '

                # Apply reverse attribute when char is selected
                if selection.contains(position):
                    reverse = True
                    # display newline character explicitly when selected
                    if char == '\n':
                        char = '↵\n'
                        #drawchar = ' \n'

                # Apply highlight attribute when char is locked
                if (self.doc.locked_selection != None
                        and self.doc.locked_selection.contains(position)):
                    highlight = True
                    # display newline character explicitly when locked
                    if char == '\n':
                        char = '↵\n'
                        #drawchar = ' \n'

                # Apply color attribute if char is labeled
                if position in labeling:
                    if labeling[position] == 'error':
                        alt_background = True
                    elif labeling[position] == 'warning':
                        alt_background = True

                    for i, label in enumerate(['string', 'number', 'keyword', 'comment']):
                        if labeling[position] == label:
                            color = 11 + i

                attribute = self.create_attribute(reverse=reverse, color=color,
                        highlight=highlight, alt_background=alt_background)

                self.draw_string(drawchar, attribute, silent=False)
                position += 1

                # Draw line numbers
                if char == '\n':
                    linenumber += 1
                    self.draw_string(str(linenumber) + (number_width - len(str(linenumber)) + 1) * ' ', numbercolor)

            except EndOfWin:
                break

