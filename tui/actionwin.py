"Module containing ActionWin class."""
import curses
from .win import Win


class ActionWin(Win):
    """Window containing the actiontree."""

    def __init__(self, width, height, x, y, session):
        Win.__init__(self, width, height, x, y, session)

    def draw(self):
        """Draw the current actiontree."""
        actiontree = self.session.actiontree
        try:
            self.win.addstr(0, 0, 'History:\n'
                            + actiontree.dump(self.height, self.width))
           # parent = (str(actiontree.current_node.parent.action) + '\n'
                     # if actiontree.current_node.parent else '')
           # current = str(self.session.actiontree.current_node.action)
           # self.win.addstr(0, 0, 'Current action:\n' + parent + current)

        except curses.error:
           # End of window reached
            pass
        self.win.clrtobot()
        self.win.refresh()
