import json
from os.path import dirname

from gi.repository import Gtk, Gdk, Gio


class CSSLoader(Gtk.CssProvider):
    def __init__(self, path: str):
        super().__init__()

        self.path = path
        self.load_from_path(self.path)

        dir = Gio.file_new_for_path(dirname(path))

        self.monitor = dir.monitor_directory(Gio.FileMonitorFlags.NONE)
        self.monitor.connect("changed", self.do_changed)

        display = Gdk.Display.get_default()
        assert display is not None

        Gtk.StyleContext.add_provider_for_display(
            display,
            self,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def do_changed(
        self,
        monitor: Gio.FileMonitor,
        file: Gio.File,
        _,
        event: Gio.FileMonitorEvent,
    ):
        if event == Gio.FileMonitorEvent.CHANGES_DONE_HINT:
            self.load_from_path(self.path)
