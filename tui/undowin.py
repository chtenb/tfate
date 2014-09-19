"Module containing ActionWin class."""
from .window import Window
from fate.undotree import UndoMode
from logging import debug


class UndoWin(Window):

    """Window containing the undotree."""

    def __init__(self, ui):
        Window.__init__(self, ui)

    def update(self):
        """We only want to be enabled if undomode is active."""
        if isinstance(self.document.mode, UndoMode) and not self.enabled:
            self.enable()
        if not isinstance(self.document.mode, UndoMode) and self.enabled:
            self.disable()

    def draw(self):
        """Draw the current commandtree.
        It should look like this, where X is the current position:
        o-o-o-o-o-X-o-o-o
            |     | ↳ o-o-o-o-o
            |     ↳ o-o-o
            ↳ o-o-o
                ↳ o-o-o
        """
        undotree = self.document.undotree
        # We only have to print height/2 children branches
        # and parents branches, and width/2 children and parents

        # So first traverse upwards until exceed height or width
        upperbound = traverse_up(undotree.current_node,
                                 int(self.height / 2) + 1,
                                 int(self.width / 2) + 1)
        # self.height, self.width)
        # Then print tree downwards until exceed height or width
        string = '\n'.join(dump(upperbound, undotree.current_node,
                                self.height, self.width))

        self.draw_line('Undo tree', self.create_attribute(reverse=True))

        center = string.find('X')
        string = self.crop(string, center)
        self.draw_string(string)


def traverse_up(node, height, width):
    """Traverse upwards until exceed height or width."""
    parent = node.parent
    if not parent or height <= 0 or width <= 0:
        return node
    else:
        return traverse_up(parent, height - len(parent.children) + 1, width - 2)


def dump(node, current_node, height, width):
    """
    Return an array with the pretty printed lines of children
    of node, until we exceed height or width.
    """
    me = 'X' if node is current_node else 'o'

    if not node.children or height <= 0 or width <= 0:
        return [me]

    result = []
    for i, child in enumerate(node.children):
        child_dump = dump(child, current_node, height, width - 2)
        height -= len(child_dump) - 1
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
                    #child_dump[j] = '↳ ' + line
                    child_dump[j] = '->' + line
                else:
                    child_dump[j] = last_child + ' ' + line

        result.extend(child_dump)
    return result
