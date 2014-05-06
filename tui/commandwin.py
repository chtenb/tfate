"Module containing StatusWin class."""
from .win import Win
from logging import debug


class CommandWin(Win):

    """Window for the command interface."""

    def __init__(self, width, height, x, y, session, ui):
        Win.__init__(self, width, height, x, y, session)
        self.ui = ui
        self.min_height = height
        self.reset()

    def reset(self):
        self.text = None
        self.completions = None
        self.hide()

    def draw(self):
        if self.text:
            self.height = max(self.min_height, int(len(self.text) / self.width))
            self.draw_line(self.text, self.create_attribute(alt_background=True))
        elif self.completions:
            for i, (name, descr) in enumerate(self.completions):
                highlight = True if self.current_completion == i else False
                attribute = self.create_attribute(highlight=highlight, alt_background=True)
                self.draw_line(name + '  ' + descr, attribute, wrapping=True)

    def prompt(self):
        """Prompt the user for a command."""
        from fate import selectors, operators, actors, uiactions

        self.scope = vars(self.session)
        self.scope.update({'self': self.session})
        self.scope.update(vars(selectors))
        self.scope.update(vars(operators))
        self.scope.update(vars(actors))
        self.scope.update(vars(uiactions))

        self.completions = [('', '')]
        self.current_completion = 0
        self.text = None

        self.show()
        self.ui.touch()
        command = self.get_command()
        if command != None:
            try:
                result = eval(command, self.scope)
            except Exception as e:
                self.text = command + ' : ' + str(e)
                self.win.getch()
            else:
                while callable(result):
                    result = result(self.session)

                if result != None:
                    self.text = str(result)
                    self.ui.touch()
                    self.ui.getchar()

        self.reset()

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

            self.ui.touch()
