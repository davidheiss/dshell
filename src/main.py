from ctypes import CDLL

import gi.repository

CDLL("libgtk4-layer-shell.so")

import gi

gi.require_versions(
    {
        "Gtk": "4.0",
        "Gtk4LayerShell": "1.0",
    }
)

from gi.repository import Gtk, GLib, Gtk4LayerShell

from app import App

MAJOR_VERSION = 0
MINOR_VERSION = 1
MICRO_VERSION = 0

def url(text: str, url):
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"

if __name__ == "__main__":
    print(
        f"""
 ____  ____    {url("DShell","https://github.com/davidheiss/dshell")} v{MAJOR_VERSION}.{MINOR_VERSION}.{MICRO_VERSION}
|  _ \\/ ___|   Copyright (C) 2024 David Heiß 
| | | \\___ \\
| |_| |___) |  This program may be freely redistributed under 
|____/|____/   the terms of the GNU General Public License.

               {url("GTK","https://www.gtk.org/")}        - v{Gtk.get_major_version()}.{Gtk.get_minor_version()}.{Gtk.get_micro_version()}
               {url("LayerShell", "https://github.com/wmww/gtk4-layer-shell")} - v{Gtk4LayerShell.get_major_version()}.{Gtk4LayerShell.get_minor_version()}.{Gtk4LayerShell.get_micro_version()}
""",
end=None
    )

    app = App()
    try:
        exit(app.run())
    except KeyboardInterrupt:
        exit(0)