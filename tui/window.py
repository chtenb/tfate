"""
Module containing Win class.
The Win class is meant to hide some common intercommand with curses.
"""
import unicurses as curses
from . import terminal
from logging import debug


class Window:

    """Abstract window class"""

    def __init__(self, ui):
        self.win = curses.newwin(0, 0, 0, 0)
        self.ui = ui
        self.document = ui.document
        self.enabled = True

    def enable(self):
        """Enable this window."""
        self.enabled = True
        self.ui.update_windows()

    def disable(self):
        """Disable this window."""
        self.enabled = False
        self.ui.update_windows()

    def reset(self, width=None, height=None, x=None, y=None):
        """Resize window."""
        if height == None:
            height = self.height
        if width == None:
            width = self.width
        if x == None:
            x = self.x
        if y == None:
            y = self.y

        curses.wresize(self.win, height, width)
        curses.mvwin(self.win, y, x)

        #debug(height)
        #debug(self.height)

        assert self.height == height
        assert self.width == width
        assert self.x == x
        assert self.y == y

    def refresh(self):
        """Refresh the window."""
        self.update()

        if self.enabled:
            curses.wmove(self.win, 0, 0)
            self.draw()
            # TODO: this causes the last character to be blank
            curses.wclrtobot(self.win)
            curses.wrefresh(self.win)

    def update(self):
        """This draw method may be overridden to keep internals in sync with the document."""
        pass

    def draw(self):
        """This draw method needs to be overridden to draw the window content."""
        pass

    @property
    def width(self):
        """Width of the window."""
        _, width = curses.getmaxyx(self.win)
        return width

    @property
    def height(self):
        """Height of the window."""
        height, _ = curses.getmaxyx(self.win)
        return height

    @property
    def x(self):
        """X coordinate of upper left corner."""
        _, x = curses.getbegyx(self.win)
        return x

    @property
    def y(self):
        """Y coordinate of upper left corner."""
        y, _ = curses.getbegyx(self.win)
        return y

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


        if not terminal.HAS_COLORS:
            if alt_background:
                result ^= curses.A_REVERSE
            if highlight:
                result ^= curses.A_REVERSE
        else:
            colorpair = color % (terminal.COLOR_PAIRS + 1)

            if alt_background:
                if terminal.HAS_BACKGROUND_COLORS:
                    colorpair = color + terminal.COLOR_PAIRS + 1
                else:
                    result ^= curses.A_REVERSE

            if highlight:
                if terminal.HAS_BACKGROUND_COLORS:
                    colorpair = color + terminal.COLOR_PAIRS + terminal.COLOR_PAIRS + 1
                else:
                    result ^= curses.A_REVERSE

            result |= curses.color_pair(colorpair)
        return result

    def draw_string(self, string, attributes=0, wrapping=False, silent=True):
        """Try to draw a string with given attributes."""
        if wrapping:
            ret = curses.waddnstr(self.win, string, self.width, attributes)
        else:
            ret = curses.waddstr(self.win, string, attributes)

        # End of window reached
        if ret == curses.ERR and not silent:
            raise EndOfWin()

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

class EndOfWin(BaseException):
    pass
