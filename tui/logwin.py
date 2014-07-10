"Module containing logging window."""
from .win import Win
from fate import LOG_QUEUE
from logging.handlers import QueueListener

class LogWin(Win):

    def __init__(self, width, height, x, y, session):
        Win.__init__(self, width, height, x, y, session)
        self.records = []
        self.listener = QueueListener(LOG_QUEUE, self.handle_record)
        self.listener.start()

    def handle_record(self, record):
        self.records.append(record)
        self.ui.touch()

    def draw(self):
        """Draw log"""
        caption = 'Log: {}, {}'.format(LOG_QUEUE.qsize(), len(self.records))
        content = ''.join(self.records[-self.height + 2:])

        self.draw_line(caption, self.create_attribute(alt_background=True))
        self.draw_line(content)
