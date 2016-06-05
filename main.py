"""Top level script which runs fate."""
import os
import sys

# Make sure fate can be imported anywhere (also from the user script).
# This way we can:
# - run fate without having it installed
# - and thus easily test development source
# - have multiple fate packages, in case we would use multiple user interfaces.
fate_path = os.path.dirname(os.path.abspath(__file__)) + '/libs/fate'
sys.path.insert(0, fate_path)

unicurses_path = os.path.dirname(os.path.abspath(__file__)) + '/libs/unicurses'
sys.path.insert(0, unicurses_path)


import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', help='run in debug mode',
                    action='store_true')
parser.add_argument('-c', '--commands',
                    help='Specify a string of keys to be fed to fate for each file')
parser.add_argument('filenames', help='filenames to be openened at startup',
                    nargs='*')
args = parser.parse_args()


# Import fate to make sure the logger is initialized
import fate
import logging

if args.debug:
    logging.getLogger().setLevel('DEBUG')
else:
    logging.getLogger().setLevel('INFO')


# Use fate either in batch mode or interactively
if args.commands:
    from batch import batch
    batch(args.filenames, args.commands)
else:
    from tui import start
    start(args.filenames)
