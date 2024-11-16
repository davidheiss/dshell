from gi.repository import Gtk, Gdk, Gtk4LayerShell as LayerShell


class Panel(Gtk.ApplicationWindow):
    def __init__(
        self,
        application: Gtk.Application,
        monitor: Gdk.Monitor | None = None,
    ):
        super().__init__(application=application)

        self.set_default_size(0, 45)

        LayerShell.init_for_window(self)

        if isinstance(monitor, Gdk.Monitor):
            LayerShell.set_monitor(monitor)

        LayerShell.set_anchor(self, LayerShell.Edge.LEFT, True)
        LayerShell.set_anchor(self, LayerShell.Edge.TOP, True)
        LayerShell.set_anchor(self, LayerShell.Edge.RIGHT, True)

        LayerShell.auto_exclusive_zone_enable(self)
