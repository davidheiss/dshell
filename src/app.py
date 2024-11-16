from gi.repository import Gtk

from windows.panel import Panel


class App(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="com.github.davidheiss.dshell",
        )

    def do_activate(self):
        self.panel = Panel(self)
        self.panel.present()