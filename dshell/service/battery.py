import os

from gi.repository import GObject, GLib # type: ignore

from .service import Service

SIGNALS = {
    "capacity": (GObject.SignalFlags.RUN_FIRST, None, (int,)),
}

class BatteryService(Service):
    __gsignals__ = SIGNALS

    def __init__(self):
        super().__init__()

        self.capacity: int = None

        self.update()
        GLib.timeout_add_seconds(1, self.update)


    def update(self):
        path = "/sys/class/power_supply/BAT0/capacity"
        if not os.path.exists(path):
            return False

        with open(path) as file:
            capacity = int(file.read().strip())
        
        if self.capacity != capacity:
            self.emit("capacity", capacity)

        self.capacity = capacity

        return True