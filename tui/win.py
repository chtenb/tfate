"""
Module containing Win class.
The Win class is meant to hide some common interaction with curses.
"""
import curses


class Win():
    """Abstract window class"""

    def __init__(self, width, height, x, y, session):
        self.win = curses.newwin(height, width, y, x)
        self.session = session

    def draw(self):
        """Draw the window."""
        self.win.refresh()

    def draw_focused_string(self, string, n):
        """Draw string with focus on nth character."""
        height, width = self.win.getmaxyx()

        self.win.move(0, 0)


