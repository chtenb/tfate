"""Module containing logging window."""
from .window import Window
from fate import LOG_QUEUE
from logging.handlers import QueueListener
from logging import Handler


class LogWin(Window, Handler):

    """
    This window acts as a logging handler by storing all incoming records into list,
    which is printed on the screen in the draw method of this window.
    """

    def __init__(self, ui):
        Window.__init__(self, ui)
        Handler.__init__(self)
        self.records = []
        self.listener = QueueListener(LOG_QUEUE, self)
        self.listener.start()

    def emit(self, record):
        self.records.append(record)
        self.ui.touch()

    def draw(self):
        """Draw log"""
        #caption = 'Log: {}, {}'.format(LOG_QUEUE.qsize(), len(self.records))
        #self.draw_line(caption, self.create_attribute(alt_background=True))
        for r in self.records[-self.height:]:
            self.draw_line(r.message, self.create_attribute(reverse=True))
