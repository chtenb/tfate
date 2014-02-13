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

    def refresh(self):
        """Refresh the window."""
        self.win.move(0, 0)
        self.draw()
        self.win.clrtobot()
        self.win.refresh()

    def draw(self):
        """This draw method needs to be overridden."""
        pass

    def draw_string(self, string, attributes=None):
        """Try to draw a string with given attributes."""
        try:
            if attributes:
                self.win.addstr(string, attributes)
            else:
                self.win.addstr(string)
        except curses.error:
            # End of window reached
            pass

    def draw_line(self, string, attributes=None):
        """Try to draw string ending with an eol."""
        self.draw_string(string + '\n', attributes)

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

    @property
    def x(self):
        """X coordinate of upper left corner."""
        _, x = self.win.getbegyx()
        return x

    @property
    def y(self):
        """Y coordinate of upper left corner."""
        y, _ = self.win.getbegyx()
        return y

