"Module containing logging window."""
from .win import Win
from threading import Thread
from time import sleep
from fate import LOGFILENAME


class LogWin(Win):

    def __init__(self, width, height, x, y, session):
        Win.__init__(self, width, height, x, y, session)
        self.records = []

        self.where = 0
        self.logchecker_thread = Thread(target=self.listen)
        self.logchecker_thread.start()

    def listen(self):
        with open(LOGFILENAME, 'r') as self.f:
            while self.ui.active and self.visible:
                self.check()
                sleep(0.1)

    def check(self):
        assert self.visible
        assert self.f != None

        self.f.seek(self.where)
        while 1:
            line = self.f.readline()
            if not line:
                break
            self.records.append(line)

            # Make sure the UI thread will display incoming logs
            self.ui.touch()
        self.where = self.f.tell()

    def draw(self):
        """Draw log"""
        caption = 'Log'
        content = ''.join(self.records[-self.height + 2:])

        self.draw_line(caption, self.create_attribute(alt_background=True))
        self.draw_line(content)
