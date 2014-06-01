"""
Module containing Win class.
The Win class is meant to hide some common interaction with curses.
"""
import unicurses as curses
from logging import debug


class Win:

    """Abstract window class"""

    def __init__(self, width, height, x, y, session):
        self.win = curses.newwin(height, width, y, x)
        self.session = session
        self.ui = session.ui
        self.visible = True

    def resize(self, width=None, height=None):
        self.win.resize(height, width)

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

    @height.setter
    def height(self, value):
        self.resize(self.width, value)

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

    def hide(self):
        """Prevent self from being drawn."""
        self.visible = False

    def show(self):
        """Don't prevent self from being drawn."""
        self.visible = True

    def create_attribute(self, reverse=False, underline=False, bold=False,
                         color=0, alt_background=False, highlight=False):
        """
        Return the attribute corresponding to the given properties.
        """
        result = 0
        if bold:
            result |= curses.A_BOLD
        if underline:
            result |= curses.A_UNDERLINE
        if reverse:
            result |= curses.A_REVERSE


        if not self.ui.has_colors:
            if alt_background:
                result ^= curses.A_REVERSE
            if highlight:
                result ^= curses.A_REVERSE
        else:
            colorpair = color % (self.ui.color_pairs + 1)

            if alt_background:
                if self.ui.has_background_colors:
                    colorpair = color + self.ui.color_pairs + 1
                else:
                    result ^= curses.A_REVERSE

            if highlight:
                if self.ui.has_background_colors:
                    colorpair = color + self.ui.color_pairs + self.ui.color_pairs + 1
                else:
                    result ^= curses.A_REVERSE

            result |= curses.color_pair(colorpair)
        return result

    def refresh(self):
        """Refresh the window."""
        if self.visible:
            self.win.move(0, 0)
            self.draw()
            self.win.clrtobot()
            self.win.refresh()

    def draw(self):
        """This draw method needs to be overridden to draw the window content."""
        pass

    def draw_string(self, string, attributes=0, wrapping=False, silent=True):
        """Try to draw a string with given attributes."""
        try:
            if wrapping:
                success = self.win.addnstr(string, self.width, attributes)
            else:
                success = self.win.addstr(string, attributes)
        except:
            # End of window reached
            if not silent:
                raise

    def draw_line(self, string, attributes=0, wrapping=False, silent=True):
        """Try to draw string ending with an eol."""
        self.draw_string(string, attributes, wrapping, silent)
        self.draw_string(
            ''.join([' ' for _ in range(self.width - len(string))]), attributes)

    @staticmethod
    def get_coords(lines, pos):
        """Compute the coordinates of pos in lines."""
        y = 0
        line_beg = 0
        for line in lines:
            if pos <= line_beg + len(line):
                break
            y += 1
            line_beg += len(line)

        x = (pos - line_beg)

        return x, y

    def crop(self, string, center):
        """Crop the string around center."""
        assert 0 <= center < len(string)
        lines = string.split('\n')

        # Compensate for splitting
        center -= len(lines) - 1

        # Compute the coordinates of center
        x, y = self.get_coords(lines, center)

        # Crop vertically
        yoffset = max(0, y - int(self.height / 2))
        lines = [line for i, line in enumerate(lines) if yoffset <= i < self.height]

        # Crop horizontally
        xoffset = max(0, x - int(self.width / 2))
        lines = [line[xoffset:xoffset + self.width - 1] for line in lines]

        return '\n'.join(lines)
