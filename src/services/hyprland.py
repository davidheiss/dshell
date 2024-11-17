import os
import socket
import json
from typing import Any, Dict, List
from gi.repository import Gio, GObject, Gtk

HYPRLAND_INSTANCE_SIGNATURE = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")
XDG_RUNTIME_DIR = os.environ.get("XDG_RUNTIME_DIR")

SOCKET1 = f"{XDG_RUNTIME_DIR}/hypr/{HYPRLAND_INSTANCE_SIGNATURE}/.socket.sock"
SOCKET2 = f"{XDG_RUNTIME_DIR}/hypr/{HYPRLAND_INSTANCE_SIGNATURE}/.socket2.sock"


class Workspace:
    def __init__(
        self,
        id: int,
        name: str,
        monitor: str = None,
        monitor_id: int = None,
        windows: int = None,
        hasfullscreen: bool = None,
        lastwindow: str = None,
        lastwindowtitle: str = None,
    ):
        self.id = id
        self.name = name
        self.monitor = monitor
        self.monitor_id = monitor_id
        self.windows = windows
        self.hasfullscreen = hasfullscreen
        self.lastwindow = lastwindow
        self.lastwindowtitle = lastwindowtitle

    @classmethod
    def from_json(cls, json: Dict[str, Any]):
        return cls(
            id=json["id"],
            name=json["name"],
            monitor=json["monitor"],
            monitor_id=json["monitorID"],
            windows=json["windows"],
            hasfullscreen=json["hasfullscreen"],
            lastwindow=json["lastwindow"],
            lastwindowtitle=json["lastwindowtitle"],
        )

    def __repr__(self):
        return f"Workspace({self.monitor},{self.name})"


class Hyprland(GObject.GObject):
    @staticmethod
    def instance() -> "Hyprland":
        return Gtk.Application.get_default().hyprland

    __gsignals__ = {
        "workspacev2": (GObject.SignalFlags.RUN_FIRST, None, (str, str)),
        "createworkspacev2": (GObject.SignalFlags.RUN_FIRST, None, (str, str)),
        "destroyworkspacev2": (GObject.SignalFlags.RUN_FIRST, None, (str, str)),
    }

    def __init__(self):
        super().__init__()
        address = Gio.UnixSocketAddress.new(SOCKET2)
        connection = Gio.UnixConnection(
            socket=Gio.Socket.new(
                Gio.SocketFamily.UNIX,
                Gio.SocketType.STREAM,
                Gio.SocketProtocol.DEFAULT,
            )
        )
        connection.connect_async(address, None, self.on_connection)

    def on_data(self, input_stream: Gio.DataInputStream, result: Gio.Task):
        input_stream.read_line_async(-1, None, self.on_data)
        bytes, _ = input_stream.read_line_finish(result)
        event, message = bytes.decode().split(">>")
        if event in GObject.signal_list_names(Hyprland):
            self.emit(event, *message.split(","))

    def on_connection(self, connection: Gio.UnixConnection, result: Gio.Task):
        if connection.connect_finish(result):
            input_stream = Gio.DataInputStream.new(connection.get_input_stream())
            input_stream.read_line_async(-1, None, self.on_data)
        else:
            raise "No Hyprland Socket2 connection!"

    @staticmethod
    def command(cmd: str):
        client = socket.socket(
            socket.AddressFamily.AF_UNIX,
            socket.SocketKind.SOCK_STREAM,
        )
        client.connect(SOCKET1)
        client.send(
            f"[-j]/{cmd}".encode(),
        )
        message = client.recv(4096)
        client.close()
        return json.loads(message)

    @staticmethod
    def workspaces():
        return list(map(Workspace.from_json, Hyprland.command("workspaces")))

    @staticmethod
    def active_workspace():
        return Workspace.from_json(Hyprland.command("activeworkspace"))