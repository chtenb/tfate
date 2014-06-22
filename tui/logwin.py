"Module containing logging window."""
from .win import Win
from threading import Thread
from time import sleep
from fate import LOGFILENAME


class LogWin(Win):

    def __init__(self, width, height, x, y, session):
        Win.__init__(self, width, height, x, y, session)
        self.records = []

        self.refresh_rate = 10
        self.where = 0

        # TODO: revise this
        #self.activate()

    def activate(self):
        self.logchecker_thread = Thread(target=self._listen)
        self.logchecker_thread.start()

    def _listen(self):
        with open(LOGFILENAME, 'r') as self.f:
            self._check()
            sleep(1 / self.refresh_rate)

    def _check(self):
        assert self.f != None

        self.f.seek(self.where)
        while 1:
            line = self.f.readline()
            if not line:
                break
            self.records.append(line)

            # Make sure the UI thread will display incoming logs
            self.ui.touch()

        # Remember where we are in the file
        self.where = self.f.tell()

    def draw(self):
        """Draw log"""
        #caption = 'Log: ' + str('alive' if self.logchecker_thread.is_alive() else 'dead')
        caption = 'Log: ' + 'dead'
        content = ''.join(self.records[-self.height + 2:])

        self.draw_line(caption, self.create_attribute(alt_background=True))
        self.draw_line(content)
