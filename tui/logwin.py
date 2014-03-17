"Module containing for logging window."""
import curses
from .win import Win


class LogWin(Win):

    def __init__(self, width, height, x, y, session):
        Win.__init__(self, width, height, x, y, session)

    def draw(self):
        """Draw log"""
        caption = 'Log'
