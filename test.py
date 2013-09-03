import sys
sys.path.insert(0, './ipython')
import IPython

from protexted.session import Session
from protexted.selection import Selection
from protexted import selectors, operators
import logging

def main(filename):
    s = Session(filename)
    s.selection = Selection()
    print(bool(s.selection))
    s.selection.add((3,3))
    print(bool(s.selection))
    s.selection.add((3,3))
    print(s.selection)
    s.selection.add((1,2))
    print(s.selection)
    o = operators.insert_before(s, s.selection, "Hello world!")
    s.apply(o)
    #IPython.embed()

main("foo.txt")
