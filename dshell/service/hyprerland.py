from os import environ
import json

from gi.repository import Gio, GObject  # type: ignore

from .service import Service

SIGNALS = {
    "workspacev2": (GObject.SignalFlags.RUN_FIRST, None, (str, str)),
    "createworkspacev2": (GObject.SignalFlags.RUN_FIRST, None, (str, str)),
    "destroyworkspacev2": (GObject.SignalFlags.RUN_FIRST, None, (str, str)),
    "activewindow": (GObject.SignalFlags.RUN_FIRST, None, (str, str)),
    "activewindowv2": (GObject.SignalFlags.RUN_FIRST, None, (str,)),
}


class Hyprland(Service):
    @staticmethod
    def command(command: str):
        address = Gio.UnixSocketAddress.new(
            f"{environ['XDG_RUNTIME_DIR']}/hypr/{environ['HYPRLAND_INSTANCE_SIGNATURE']}/.socket.sock"
        )
        client = Gio.SocketClient.new()
        connection = client.connect(address)
        input_stream = connection.get_input_stream()
        output_stream = connection.get_output_stream()
        output_stream.write(f"[-j]/{command}".encode())
        data = input_stream.read_bytes(4096).unref_to_data()
        return json.loads(data)

    __gsignals__ = SIGNALS

    def __init__(self):
        super().__init__()
        address = Gio.UnixSocketAddress.new(
            f"{environ['XDG_RUNTIME_DIR']}/hypr/{environ['HYPRLAND_INSTANCE_SIGNATURE']}/.socket2.sock"
        )
        client = Gio.SocketClient.new()
        client.connect_async(address, callback=self.do_connection)

    def do_connection(self, client: Gio.SocketClient, task: Gio.Task):
        connection = client.connect_finish(task)
        input_stream = Gio.DataInputStream.new(connection.get_input_stream())
        input_stream.read_line_async(-1, callback=self.do_read_all)

    def do_read_all(self, input_stream: Gio.DataInputStream, task: Gio.Task):
        line, *_ = input_stream.read_line_finish(task)
        event, values = line.decode().split(">>")
        if event in SIGNALS:
            self.emit(event, *values.split(",", 1))
        input_stream.read_line_async(-1, callback=self.do_read_all)
