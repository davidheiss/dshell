from gi.repository import GLib, Gtk  # type: ignore

from ..service import get_service, DateTime

FORMAT = r"%Y-%m-%d %H:%M"


class Date(Gtk.Label):
    def __init__(self):
        datetime = get_service(DateTime)
        super().__init__(
            label=datetime.value.format(FORMAT),
            css_classes=["date"]
        )
        datetime.connect("changed", self.do_changed)

    def do_changed(self, service: DateTime, datetime: GLib.DateTime):
        self.set_label(datetime.format(FORMAT))
