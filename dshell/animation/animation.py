from datetime import timedelta

from gi.repository import Gtk, Gdk

class Animation[T]:
    def __init__(self, value: T, widget: Gtk.Widget, duration: timedelta):
        self._id = None
        self._start = self._last_value = self.value = self._end = value
        self._widget = widget
        self._duration = duration

    def to(self, value: T):
        self._start = self.value
        self._end = value

        if self._id is not None:
            self._widget.remove_tick_callback(self._id)

        self.time = self._widget.get_frame_clock().get_frame_time()
        self._id = self._widget.add_tick_callback(self.do_tick)
    
    def do_tick(self, widget: Gtk.Widget, clock: Gdk.FrameClock):
        duration = timedelta(microseconds=clock.get_frame_time()-self.time)
        progress = min(1,duration/self._duration)

        self._last_value = self.value
        self.value: T = self._start * (1-progress) + self._end * progress

        if self.value != self._last_value:
            widget.queue_draw()

        return progress < 1