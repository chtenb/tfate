"Module containing logging window."""
from .win import Win
import logging
from logging import Handler


class LogWin(Win, Handler):

    def __init__(self, width, height, x, y, session, ui):
        Win.__init__(self, width, height, x, y, session)
        self.ui = ui

        Handler.__init__(self)
        logger = logging.getLogger()
        logger.addHandler(self)

        self.records = []

    def emit(self, record):
        self.records.append(record.getMessage())
        #self.ui.refresh()

    def draw(self):
        """Draw log"""
        caption = 'Log'
        content = '\n'.join(self.records[-self.height+1:-1])

        self.draw_line(caption, self.colorpair(0, 1))
        self.draw_line(content)
