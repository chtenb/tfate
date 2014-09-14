"Module containing StatusWin class."""
from .window import Window
from logging import debug
from fate.commandmode import get_completions, evaluate


class CommandWin(Window):

    """Window for the command interface."""

    def __init__(self, width, height, x, y, ui):
        Window.__init__(self, width, height, x, y, ui)
        self.min_height = height
        self.reset()

    def reset(self):
        self.text = None
        self.completions = None
        self.disable()

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
        self.completions = [('', '')]
        self.current_completion = 0
        self.text = None

        self.enable()
        self.ui.touch()
        command = self.get_command()
        if command != None:
            result = evaluate(self.document, command)

            if result != None:
                self.text = str(result)
                self.ui.touch()
                self.ui.getkey()

        self.reset()

    def get_command(self):
        """Get the command from the user."""
        command = ''
        while 1:
            key = self.ui.getkey()

            if key == 'Esc':
                return
            elif key == '\n':
                # Return command
                return command
            elif key == '\t' or key == 'Btab':
                # Select completion
                d = 1 if key == '\t' else -1
                self.current_completion = ((self.current_completion + d)
                                           % len(self.completions))
                command = self.completions[self.current_completion][0]
            else:
                # Update input
                if key == '\b':
                    command = command[:-1]
                else:
                    command += key

                # Update completions
                self.current_completion = 0
                self.completions = list(get_completions(self.document, command))
                self.height = max(self.min_height, len(self.completions))

            self.ui.touch()
