"Module containing StatusWin class."""
import curses
from curses.textpad import Textbox
from .win import Win
from rlcompleter import Completer
from fate import selectors, operators, actors


class CommandWin(Win):
    """Window for the command interface."""

    def __init__(self, width, height, x, y, session, ui):
        Win.__init__(self, width, height, x, y, session)
        self.win.bkgd(' ', curses.color_pair(17))
        self.ui = ui

    def draw(self):
        if self.text:
            self.draw_string(self.text, curses.color_pair(17))
        else:
            for i, (name, descr) in enumerate(self.completions):
                attributes = curses.color_pair(1 if self.current_completion == i else 17)
                self.draw_line(name + '  ' + descr, attributes, wrapping=True)

    def prompt(self):
        """Prompt the user for an input string."""
        session = self.session
        self.scope = vars(session)
        self.scope.update({'self': session})
        self.scope.update(vars(selectors))
        self.scope.update(vars(operators))
        self.scope.update(vars(actors))

        self.completer = Completer(self.scope)
        self.completions = []
        self.current_completion = 0

        self.text = None
        self.refresh()
        command = self.get_command()

        try:
            result = eval(command, self.scope)
            if callable(result):
                result = result(session)
                if callable(result):
                    result(session)
            elif result != None:
                self.text = str(result)
                self.refresh()
                self.win.getch()
        except Exception as e:
            self.text = command + ' : ' + str(e)
            self.refresh()
            self.win.getch()

    def get_command(self):
        """Get the command from the user."""
        command = ''
        while 1:
            char = self.win.get_wch()

            if char == '\n':
                # Return command
                return command
            elif char == '\t' or char == curses.KEY_BTAB:
                # Select completion
                d = 1 if char == '\t' else -1
                self.current_completion = (self.current_completion + d) % len(self.completions)
                command = self.completions[self.current_completion][0]
            else:
                # Update input
                if char == curses.KEY_BACKSPACE:
                    command = command[:-1]
                else:
                    command += char

                # Update completions
                self.current_completion = 0
                self.completions = [(command, '')]
                if command:
                    for name, obj in self.scope.items():
                        if name.startswith(command):
                            self.completions.append((name, repr(obj)))
            self.refresh()

