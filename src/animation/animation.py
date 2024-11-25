from gi.repository import Gtk, GLib
import datetime
from .functions import easeInSine

class Animation:
    def __init__(
        self,
        widget: Gtk.DrawingArea,
        duration: datetime.timedelta,
        value: float = 0,
        timing=easeInSine,
    ):
        self.widget = widget
        self.duration = duration
        self.start = value
        self.goal = value
        self.value = value
        self.id = None
        self.time = None
        self.timing = timing

    def animate(self, to: float):
        self.time = datetime.datetime.now()
        self.start = self.goal
        self.goal = to
        if self.id != None:
            self.widget.remove_tick_callback(self.id)
        self.id = self.widget.add_tick_callback(self.tick)

    def tick(self, *args):
        duration = datetime.datetime.now() - self.time
        progress = min(duration / self.duration, 1)
        self.value = self.start * (1 - self.timing(progress)) + self.goal * self.timing(
            progress
        )
        self.widget.queue_draw()
        return progress < 1

