from gi.repository import Gtk # type: ignore

from .style import CSSLoader
from .service import Manager
from .window import PanelWindow

APPLICATION_ID = "com.github.davidheiss.dshell"

class App(Gtk.Application):
    def instance():
        app: App = Gtk.Application.get_default()
        assert app is not None
        return app

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, application_id=APPLICATION_ID)

        self.css = CSSLoader("style/main.css")
        self.services = Manager()

    def do_activate(self):
        self.panel = PanelWindow(self)
        self.panel.present()
