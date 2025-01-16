from gi.repository import GLib, Gtk  # type: ignore

from ..service import get_service, Battery

class Battery(Gtk.Label):
    def __init__(self):
        battery = get_service(Battery)

        super().__init__(
            label="Bat",
            css_classes=["battery"],
        )
        # datetime.connect("changed", self.do_changed)

    def do_changed(self, service: Battery, value):
        pass
