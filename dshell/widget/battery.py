from gi.repository import GLib, Gtk  # type: ignore

from ..service import get_service, BatteryService

class Battery(Gtk.Label):
    def __init__(self):
        battery = get_service(BatteryService)

        super().__init__(
            label=f"{battery.capacity}%",
            visible=battery.capacity is not None,
            css_classes=["battery"],
        )

        battery.connect("capacity", self.do_capacity)

    def do_capacity(self, service: BatteryService, value: int):
        self.set_label(f"{value}%")
