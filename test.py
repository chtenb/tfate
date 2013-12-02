import sys
sys.path.insert(0, './ipython')
import IPython

from protexted.session import Session
from protexted.selection import Selection
from protexted import selectors, operators
import logging

def main(filename):
    s = Session(filename)
    selection = Selection(s, [(3,5), (8,9)])
    selection1 = Selection(s, [(3,5), (8,9)])
    print(selection == selection1)
    print(selection != selection1)

main("foo.txt")
