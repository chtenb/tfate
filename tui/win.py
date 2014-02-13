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

    @property
    def width(self):
        """Width of the window."""
        _, width = self.win.getmaxyx()
        return width

    @property
    def height(self):
        """Height of the window."""
        height, _ = self.win.getmaxyx()
        return height

    def draw_centered_string(self, string, n):
        """Draw string centered on nth character."""
        self.win.move(0, 0)

