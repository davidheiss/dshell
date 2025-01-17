from gi.repository import GObject, GLib  # type: ignore

from .service import Service

SIGNALS = {
    "changed": (GObject.SignalFlags.RUN_FIRST, None, (GLib.DateTime,)),
}


class DateTimeService(Service):
    __gsignals__ = SIGNALS

    def __init__(self):
        super().__init__()
        self.value = GLib.DateTime.new_now_local()
        GLib.timeout_add_seconds(1, self.do_update)

    def do_update(self):
        self.value = GLib.DateTime.new_now_local()
        self.emit("changed", self.value)
        return True
