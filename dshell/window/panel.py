from gi.repository import Gtk, Gtk4LayerShell as LayerShell # type: ignore

from ..widget import Workspace, Title, Date

HEIGHT = 32
CORNERS = 16
SPACING = 8


class PanelWindow(Gtk.ApplicationWindow):
    def __init__(self, application: Gtk.Application = None):
        super().__init__(
            application=application,
            css_classes=["unset"],
        )

        LayerShell.init_for_window(self)
        LayerShell.set_layer(self, LayerShell.Layer.BOTTOM)
        LayerShell.set_anchor(self, LayerShell.Edge.LEFT, True)
        LayerShell.set_anchor(self, LayerShell.Edge.TOP, True)
        LayerShell.set_anchor(self, LayerShell.Edge.RIGHT, True)
        LayerShell.set_exclusive_zone(self, HEIGHT)

        start = Gtk.Box(spacing=SPACING)
        center = Gtk.Box(spacing=SPACING)
        end = Gtk.Box(spacing=SPACING)

        start.append(Workspace())
        start.append(Title())

        center.append(Date())

        panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        panel.append(
            Gtk.CenterBox(
                css_classes=["panel"],
                height_request=HEIGHT,
                start_widget=start,
                center_widget=center,
                end_widget=end,
            )
        )
        panel.append(Gtk.Box(css_classes=["corner"], height_request=CORNERS))
        self.set_child(panel)
