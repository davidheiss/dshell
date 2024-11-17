from gi.repository import Gtk, Gdk, Gio
from importlib import reload, metadata
from glob import glob

import windows

import services

APPLICATION_ID = "com.github.davidheiss.dshell"

CSS_DIR = "css"
CSS_FILE = f"{CSS_DIR}/style.css"


class App(Gtk.Application):
    provider: Gtk.StyleProvider | None = None

    def __init__(self, monitor: Gdk.Monitor | None = None, *args, **kwargs):
        super().__init__(
            *args,
            application_id=APPLICATION_ID,
            flags=Gio.ApplicationFlags.FLAGS_NONE,
            **kwargs,
        )

        self.monitor = monitor

    def load_css(self):
        display = (
            self.monitor.get_display()
            if isinstance(self.monitor, Gdk.Monitor)
            else Gdk.Display.get_default()
        )

        if isinstance(self.provider, Gtk.StyleProvider):
            Gtk.StyleContext.remove_provider_for_display(display, self.provider)

        self.provider = Gtk.CssProvider()
        self.provider.load_from_file(self.css_file)
        Gtk.StyleContext.add_provider_for_display(
            display, self.provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def changed_css(
        self,
        monitor: Gio.FileMonitor,
        file: Gio.File,
        _,
        event: Gio.FileMonitorEvent,
    ):
        if event == Gio.FileMonitorEvent.CHANGES_DONE_HINT:
            self.load_css()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        self.css_file = Gio.file_new_for_path(CSS_FILE)

        dir = Gio.file_new_for_path(CSS_DIR)
        self.css_monitor = dir.monitor_directory(Gio.FileMonitorFlags.NONE)
        self.css_monitor.connect("changed", self.changed_css)

        self.load_css()

        self.hyprland = services.Hyprland()

    def do_activate(self):
        windows.Panel(
            self,
            self.monitor,
        ).present()

