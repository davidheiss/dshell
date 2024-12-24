from gi.repository import Gtk, Gdk, Gtk4LayerShell as LayerShell  # type: ignore

from . import __version__


def url(text, url):
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"


def gtk_version():
    return url(
        f"{Gtk.get_major_version()}.{Gtk.get_minor_version()}.{Gtk.get_micro_version()}",
        "https://www.gtk.org/",
    )


def layer_shell_version():
    return url(
        f"{LayerShell.get_major_version()}.{LayerShell.get_minor_version()}.{LayerShell.get_micro_version()}",
        "https://github.com/wmww/gtk4-layer-shell",
    )


def print_version():
    print(
        f"┌─────╮╭─────╮ DShell v{__version__}                          ",
        r"│ ┌─╮ ││ ╭───╯ Copyright (C) 2024 David Heiß                  ",
        r"│ │ │ ││ ╰───╮                                                ",
        r"│ │ │ │╰───╮ │ This program may be freely redistributed under ",
        r"│ └─╯ │╭───╯ │ the terms of the GNU General Public License.   ",
        r"└─────╯╰─────╯                                                ",
        f"               GTK        - v{gtk_version()}",
        f"               LayerShell - v{layer_shell_version()}",
        sep="\n",
    )