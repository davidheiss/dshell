__author__ = "David Heiß"
__version__ = "0.1.0"

from ctypes import CDLL

import gi

CDLL("libgtk4-layer-shell.so")

gi.require_versions(
    {
        "Gtk": "4.0",
        "Gtk4LayerShell": "1.0",
    }
)
