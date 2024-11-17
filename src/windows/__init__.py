from types import ModuleType
from .panel import Panel

from gi.repository import Gtk, Gio, GLib
import importlib

def dyn_window(module: ModuleType, name: str, callback, *args, **kwargs) -> Gtk.ApplicationWindow:
    file = Gio.file_new_for_path(module.__file__)
    monitor = file.monitor_file(Gio.FileMonitorFlags.NONE)
    monitor.connect("changed", callback)
    return monitor

