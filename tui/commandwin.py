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
        self.ui = ui

    def draw(self):
        self.win.bkgd(' ', curses.color_pair(17))
        if self.text:
            self.draw_string(self.text, curses.color_pair(17))
        else:
            for i, completion in enumerate(self.completions):
                attributes = curses.color_pair(1 if self.current_completion == i else 17)
                self.draw_line(completion, attributes)

    def prompt(self):
        """Prompt the user for an input string."""
        session = self.session
        scope = vars(session)
        scope.update({'self': session})
        scope.update(vars(selectors))
        scope.update(vars(operators))
        scope.update(vars(actors))

        self.completer = Completer(scope)
        self.completions = []
        self.current_completion = 0

        self.text = None
        self.refresh()
        command = self.get_command()

        try:
            result = eval(command, scope)
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
        result = ''
        while 1:
            char = self.win.get_wch()

            if char == '\n':
                # Return command
                return result
            elif char == '\t' or char == curses.KEY_BTAB:
                # Select completion
                d = 1 if char == '\t' else -1
                self.current_completion = (self.current_completion + d) % len(self.completions)
                result = self.completions[self.current_completion]
            else:
                # Update input and completions
                if char == curses.KEY_BACKSPACE:
                    result = result[:-1]
                else:
                    result += char
                self.current_completion = 0
                i = 0
                self.completions = [result]
                while 1:
                    completion = self.completer.complete(result, i)
                    if not completion:
                        break
                    self.completions.append(completion)
                    i += 1
            self.refresh()

