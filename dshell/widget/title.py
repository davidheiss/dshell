from gi.repository import Gtk, Pango # type: ignore

from ..service import get_service, HyprlandService


class Title(Gtk.Label):
    def __init__(self):
        super().__init__(
            label=HyprlandService.command("activewindow").get("title"),
            css_classes=["title"],
            max_width_chars=32,
            ellipsize=Pango.EllipsizeMode.END,
        )

        get_service(HyprlandService).connect("activewindow", self.do_activewindow)

    def do_activewindow(self, service: HyprlandService, class_: str, name: str):
        self.set_label(name)
        self.queue_draw()
