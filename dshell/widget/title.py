from gi.repository import Gtk, Pango # type: ignore

from ..service import get_service, Hyprland


class Title(Gtk.Label):
    def __init__(self):
        super().__init__(
            label=Hyprland.command("activewindow").get("title"),
            css_classes=["title"],
            max_width_chars=32,
            ellipsize=Pango.EllipsizeMode.END,
        )

        get_service(Hyprland).connect("activewindow", self.do_activewindow)

    def do_activewindow(self, service: Hyprland, class_: str, name: str):
        self.set_label(name)
        self.queue_draw()
