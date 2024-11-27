from gi.repository import Gtk, GLib
from datetime import datetime, timedelta
from typing import Callable
from .functions import easeInSine


class Animation:
    def __init__(
        self,
        widget: Gtk.DrawingArea,
        duration: timedelta,
        value: float = 0,
        timing: Callable[[float], float] = easeInSine,
        on_done: Callable = None,
    ):
        self.id = None
        self.widget = widget
        self.duration = duration
        self.value = value
        self.timing = timing
        self.on_done = on_done

    def __rmul__(self, lhs: float):
        return lhs * self.value

    def set(self, value: float):
        pass

    def animate(self, value: float):
        self.start = self.value
        self.end = value
        self.start_time = datetime.now()
        if self.id is not None:
            self.widget.remove_tick_callback(self.id)
        self.widget.add_tick_callback(self.tick)

    def tick(self, *args):
        now = datetime.now()
        duration = now - self.start_time

        progress = min(duration / self.duration,1)
        timing = self.timing(progress)
        self.value = self.start*(1-timing) + self.end*timing

        self.widget.queue_draw()

        is_done = progress == 1
        return not is_done
