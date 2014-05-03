"Module containing StatusWin class."""
from .win import Win
from logging import debug
import curses


class CommandWin(Win):

    """Window for the command interface."""

    def __init__(self, width, height, x, y, session, ui):
        Win.__init__(self, width, height, x, y, session)
        self.win.bkgd(' ', self.colorpair(0, 1))
        self.ui = ui
        self.min_height = height

    def draw(self):
        if self.text:
            self.height = max(self.min_height, int(len(self.text) / self.width))
            self.draw_string(self.text, self.colorpair(0, 1))
        else:
            for i, (name, descr) in enumerate(self.completions):
                attributes = self.colorpair(14 if self.current_completion == i else 0, 1)
                self.draw_line(name + '  ' + descr, attributes, wrapping=True)

    def prompt(self):
        """Prompt the user for an input string."""
        from fate import selectors, operators, actors, ui_actions

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
            while callable(result):
                result = result(self.session)

            if result != None:
                self.text = str(result)
                self.refresh()
                self.ui.refresh()
                self.win.getch()

    def get_command(self):
        """Get the command from the user."""
        command = ''
        while 1:
            char = self.ui.getchar()

            if char == 'Esc':
                return
            elif char == '\n':
                # Return command
                return command
            elif char == '\t' or char == 'Btab':
                # Select completion
                d = 1 if char == '\t' else -1
                self.current_completion = ((self.current_completion + d)
                                           % len(self.completions))
                command = self.completions[self.current_completion][0]
            else:
                # Update input
                if char == '\b':
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

            self.ui.refresh()
            self.refresh()
