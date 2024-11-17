from gi.repository import Gtk, Gdk, Gtk4LayerShell as LayerShell

HEIGHT = 38

from widgets.panel import Workspaces


class Corners(Gtk.Widget):
    def __init__(self):
        super().__init__()
        self.set_size_request(-1, 16)
        self.add_css_class("corners")


class Container(Gtk.CenterBox):
    def __init__(self):
        super().__init__()
        self.set_size_request(-1, HEIGHT)
        self.add_css_class("container")

        start_box = Gtk.Box(hexpand=True)
        start_box.append(Workspaces())
        self.set_start_widget(start_box)


class Panel(Gtk.ApplicationWindow):
    def __init__(
        self,
        application: Gtk.Application,
        monitor: Gdk.Monitor | None = None,
    ):
        super().__init__(
            application=application,
        )

        self.set_default_size(0, HEIGHT)

        self.add_css_class("panel")

        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
        )
        box.append(Container())
        box.append(Corners())
        self.set_child(box)

        LayerShell.init_for_window(self)
        if isinstance(monitor, Gdk.Monitor):
            LayerShell.set_monitor(monitor)
        LayerShell.set_layer(self, LayerShell.Layer.BOTTOM)
        LayerShell.set_anchor(self, LayerShell.Edge.LEFT, True)
        LayerShell.set_anchor(self, LayerShell.Edge.TOP, True)
        LayerShell.set_anchor(self, LayerShell.Edge.RIGHT, True)
        LayerShell.set_exclusive_zone(self, HEIGHT)
