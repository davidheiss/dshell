from gi.repository import GObject, Gio # type: ignore

from .service import Service

SIGNALS = {
    "changed": (GObject.SignalFlags.RUN_FIRST, None, (float,)),
}

class Battery(Service):
    __gsignals__ = SIGNALS

    def __init__(self):
        super().__init__()

        path = "class/power_supply/BAT0"
        dir = Gio.file_new_for_path(path)

        self._monitor = dir.monitor_directory(Gio.FileMonitorFlags.NONE)
        self._monitor.connect("changed", self.do_changed)
    
    def do_changed(self, *args):
        print(args)

        

