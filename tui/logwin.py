"Module containing logging window."""
import curses
from .win import Win
import logging
from logging import Handler


class LogWin(Win, Handler):

    def __init__(self, width, height, x, y, session):
        Win.__init__(self, width, height, x, y, session)

        Handler.__init__(self)
        logger = logging.getLogger()
        logger.addHandler(self)

        self.records = []

    def emit(self, record):
        self.records.append(record.getMessage())

    def draw(self):
        """Draw log"""
        caption = 'Log'
        content = '\n'.join(self.records)

        self.draw_line(caption, curses.color_pair(17))
        self.draw_line(content)
