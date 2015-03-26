"""Module containing CompletionWin class."""
from .window import Window
from fate.insertoperations import Completable
import math


class CompletionWin(Window):

    """Window containing the completions."""

    def __init__(self, ui):
        Window.__init__(self, ui)

    def update(self):
        """We only want to be enabled if insertmode has completions."""
        if (isinstance(self.document.mode, Completable) and self.document.mode.completions
                and not self.enabled):
            self.enable()
        if not isinstance(self.document.mode, Completable) and self.enabled:
            self.disable()

    def draw(self):
        completions = self.document.mode.completions
        selected_completion = self.document.mode.selected_completion
        nr_completions = len(completions)

        self.draw_line('Completions', self.create_attribute(alt_background=True))

        # Window slice pattern
        show_before = math.ceil((self.height - 2) / 2)
        show_after = math.floor((self.height - 2) / 2)
        before_left_over = max(0, show_before - selected_completion)
        after_left_over = max(0, show_after - (nr_completions - selected_completion - 1))
        show_start = max(0, selected_completion - show_before - after_left_over)
        show_end = min(nr_completions, selected_completion + show_after +
                       before_left_over + 1)

        for i in range(show_start, show_end):
            completion = completions[i]
            attribute = self.create_attribute()
            if selected_completion == i:
                attribute = self.create_attribute(reverse=True)
            self.draw_line(str(completion), attribute)
