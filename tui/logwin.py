"""Module containing logging window."""
from .window import Window
from fate import log

class LogWin(Window):

    """
    This window acts as a logging handler by storing all incoming records into list,
    which is printed on the screen in the draw method of this window.
    """

    def __init__(self, ui):
        Window.__init__(self, ui)

    def draw(self):
        """Draw log"""
        #caption = 'Log: {}, {}'.format(LOG_QUEUE.qsize(), len(self.records))
        #self.draw_line(caption, self.create_attribute(alt_background=True))
        for r in log.RECORDS[-self.height:]:
            self.draw_line(r.message, self.create_attribute(reverse=True))
