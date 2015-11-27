"Module containing TextWin class."""
from .window import Window, EndOfWin
from logging import info


class TextWin(Window):

    """Window containing the text"""

    def __init__(self, ui):
        Window.__init__(self, ui)
        self.offset = 0

    def draw_empty_interval(self):
        try:
            self.draw_string('ε', self.create_attribute(reverse=True), silent=False)
        except UnicodeEncodeError:
            self.draw_string('|', self.create_attribute(reverse=True), silent=False)

    def draw(self):
        """Draw the visible text in the text window."""
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
                    self.draw_empty_interval()
                    del empty_interval_positions[0]

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

                # Apply reverse attribute when char is selected
                reverse = False
                if selectionview.contains(pos):
                    reverse = True
                    # display newline character explicitly when selected
                    if char == '\n':
                        # char = '↵\n'
                        char = ' \n'
                        #drawchar = ' \n'

                attribute = self.create_attribute(reverse=reverse, color=color,
                            highlight=False, alt_background=alt_background)
                self.draw_string(char, attribute, silent=False)

            # If we come here, the entire textview fits on the screen
            # Draw possible remaining empty interval
            if empty_interval_positions:
                    self.draw_empty_interval()
            # Draw EOF character
            self.draw_line('EOF', self.create_attribute(bold=True), silent=False)
        except EndOfWin:
            pass

