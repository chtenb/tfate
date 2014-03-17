"""
Module containing Win class.
The Win class is meant to hide some common interaction with curses.
"""
import curses


class Win:
    """Abstract window class"""

    def __init__(self, width, height, x, y, session):
        self.win = curses.newwin(height, width, y, x)
        self.win.keypad(1)
        self.session = session

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

    def refresh(self):
        """Refresh the window."""
        self.win.move(0, 0)
        self.draw()
        self.win.clrtobot()
        self.win.refresh()

    def draw(self):
        """This draw method needs to be overridden to draw the window content."""
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
        self.draw_string(string, attributes)
        self.draw_string(''.join([' ' for _ in range(self.width - len(string))]), attributes)

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

        # logging.debug(str((x, y)))
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

