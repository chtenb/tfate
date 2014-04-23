"Module containing StatusWin class."""
import curses
from .win import Win


class CommandWin(Win):

    """Window for the command interface."""

    def __init__(self, width, height, x, y, session, ui):
        Win.__init__(self, width, height, x, y, session)
        self.win.bkgd(' ', curses.color_pair(17))
        self.ui = ui
        self.min_height = height

    def draw(self):
        if self.text:
            self.height = max(self.min_height, int(len(self.text) / self.width))
            self.draw_string(self.text, curses.color_pair(17))
        else:
            for i, (name, descr) in enumerate(self.completions):
                attributes = curses.color_pair(31 if self.current_completion == i else 17)
                self.draw_line(name + '  ' + descr, attributes, wrapping=True)

    def prompt(self):
        """Prompt the user for an input string."""
        from . import ui_actions
        from fate import selectors, operators, actors

        self.scope = vars(self.session)
        self.scope.update({'self': self.session})
        self.scope.update(vars(selectors))
        self.scope.update(vars(operators))
        self.scope.update(vars(actors))
        self.scope.update(vars(ui_actions))

        self.completions = [('', '')]
        self.current_completion = 0

        self.text = None
        self.refresh()
        command = self.get_command()
        if command == None:
            return

        try:
            result = eval(command, self.scope)
        except Exception as e:
            self.text = command + ' : ' + str(e)
            self.refresh()
            self.win.getch()
        else:
            # We find out whether we have a ui action or a session action by trying
            # TODO change this! It doesn't work often
            for argument in [self.session, self.ui]:
                try:
                    while callable(result):
                        result = result(argument)

                    if result != None:
                        self.text = str(result)
                        self.refresh()
                        self.win.getch()
                except (TypeError, AttributeError):
                    pass

    def get_command(self):
        """Get the command from the user."""
        command = ''
        while 1:
            char = self.win.get_wch()

            if char == '\x1b':
                return
            elif char == '\n':
                # Return command
                return command
            elif char == '\t' or char == curses.KEY_BTAB:
                # Select completion
                d = 1 if char == '\t' else -1
                self.current_completion = ((self.current_completion + d)
                                           % len(self.completions))
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
                        if name.lower().startswith(command.lower()):
                            self.completions.append((name, repr(obj)))
                self.height = max(self.min_height, len(self.completions))
            self.ui.text_win.refresh()
            self.refresh()
