"Module containing ActionWin class."""
import curses
from .win import Win


class ActionWin(Win):
    """Window containing the actiontree."""

    def __init__(self, width, height, x, y, session):
        Win.__init__(self, width, height, x, y, session)

    def draw(self):
        """Draw the current actiontree.
        It should look like this, where X is the current position:
        o-o-o-o-o-X-o-o-o
            |     | ↳ o-o-o-o-o
            |     ↳ o-o-o
            ↳ o-o-o
                ↳ o-o-o
        """
        actiontree = self.session.actiontree
        # We only have to print height/2 children branches
        # and parents branches, and width/2 children and parents

        # So first traverse upwards until exceed height or width
        upperleft = traverse_up(actiontree.current_node, int(self.height / 2), int(self.width / 2))
        # Then print tree downwards until exceed height or width
        string = '\n'.join(dump(upperleft, actiontree.current_node, self.height, self.width))

        try:
            self.win.addstr(0, 0, 'History:\n' + string)
           # parent = (str(actiontree.current_node.parent.action) + '\n'
                     # if actiontree.current_node.parent else '')
           # current = str(self.session.actiontree.current_node.action)
           # self.win.addstr(0, 0, 'Current action:\n' + parent + current)

        except curses.error:
           # End of window reached
            pass
        self.win.clrtobot()
        self.win.refresh()


def traverse_up(node, height, width):
    """Traverse upwards until exceed height or width."""
    if not node.parent or height <= 0 or width <= 0:
        return node
    elif len(node.parent.children) == 1:
        return traverse_up(node.parent, height, width - 2)
    else:
        return traverse_up(node.parent, height - 1, width - 2)


def dump(node, current_node, height=0, width=0):
    """
    Return an array with the pretty printed lines of children
    of node, until we exceed height or width.
    """
    me = 'X' if node is current_node else 'o'

    if not node.children:
        return [me]

    result = []
    for i, child in enumerate(node.children):
        child_dump = dump(child, current_node, height, width - 2)
        height -= len(child_dump)
        last_child = '|' if i < len(node.children) - 1 else ' '

        if i == 0:
            for j, line in enumerate(child_dump):
                if j == 0:
                    child_dump[j] = me + '-' + line
                else:
                    child_dump[j] = last_child + ' ' + line
        else:
            for j, line in enumerate(child_dump):
                if j == 0:
                    child_dump[j] = '↳ ' + line
                else:
                    child_dump[j] = last_child + ' ' + line

        result.extend(child_dump)
    return result
