"""Module containing TextWin class."""
from logging import info, debug

# This also loads conceal.py, such that we know for sure that this is initialized before
# we do stuff.
from fate.textview import TextView
from fate.document import Document
from fate.selection import Interval

from .window import Window, EndOfWin

# Since we are in a terminal, we are limited by textonly information
# Therefore we want to add meta information in the form of text


def init_concealers(doc):
    # We know that conceal stuff has been initialized, since TextView is imported
    doc.OnGenerateLocalConceal.add(show_empty_interval_selections)
    doc.OnGenerateLocalConceal.add(show_selected_newlines)
    # FIXME: for some reason this causes the screen thread to hang somewhere
    # doc.OnGenerateLocalConceal.add(show_eof)

Document.OnDocumentInit.add(init_concealers)


# TODO: different highlighting for empty interval selections?
# TODO: Make sure it is in view selection
def show_empty_interval_selections(doc, start_pos, max_length):
    for beg, end in doc.selection:
        if beg == end and start_pos <= beg <= start_pos + max_length:
            doc.conceal.local_substitute(Interval(beg, end), '|')


def show_selected_newlines(doc, start_pos, max_length):
    for beg, end in doc.selection:
        for pos, char in enumerate(doc.text[beg:end]):
            if char == '\n':
                doc.conceal.local_substitute(Interval(beg + pos, beg + pos + 1), ' \n')


def show_eof(doc, start_pos, max_length):
    textlength = len(doc.text)
    doc.conceal.local_substitute(Interval(textlength, textlength), 'EOF')


class TextWin(Window):

    """Window containing the text"""

    def __init__(self, ui):
        Window.__init__(self, ui)
        self.offset = 0

    def draw(self):
        """Draw the visible text in the text window."""
        # TODO: allow line numbers. Maybe should be done by concealments
        # Compute the line number of the first line
        #number_of_lines = text.count('\n', 0) + 1
        #number_width = len(str(number_of_lines))
        #linenumber = text.count('\n', 0, position) + 1
        #numbercolor = self.create_attribute(color=2)
        # self.draw_string(str(linenumber) + (number_width - len(str(linenumber)) + 1) * ' ',
        # numbercolor)

        self.textview = TextView(self.doc, self.width, self.height, self.offset)
        text = self.textview.text

        highlightingview = self.textview.highlighting
        selectionview = self.textview.selection

        try:
            for pos, char in enumerate(text):
                # Apply reverse attribute when char is selected
                reverse = False
                if selectionview.contains(pos):
                    reverse = True

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

                attribute = self.create_attribute(reverse=reverse,
                                                  color=color,
                                                  highlight=False,
                                                  alt_background=alt_background)
                self.draw_string(char, attribute, silent=False)
        except EndOfWin:
            pass
