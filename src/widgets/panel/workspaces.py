import cairo
from cairo import Context
from gi.repository import Gtk, GLib
from services import Hyprland
from enum import Enum
import math
import datetime

from windows.panel import HEIGHT

WORKSPACE_COUNT = 5
WORKSPACE_SIZE = 16
WORKSPACE_SPACING = 4


class Animation:
    def __init__(
        self,
        widget: Gtk.DrawingArea,
        duration: datetime.timedelta,
        value: float = 0,
    ):
        self.widget = widget
        self.duration = duration
        self.start = value
        self.goal = value
        self.value = value
        self.id = None
        self.time = None

    def animate(self, to: float):
        self.time = datetime.datetime.now()
        self.start = self.goal
        self.goal = to
        if self.id != None:
            self.widget.remove_tick_callback(self.id)
        self.id = self.widget.add_tick_callback(self.tick)

    def tick(self, *args):
        duration = datetime.datetime.now() - self.time
        progress = min(duration / self.duration, 1)
        self.value = self.start * (1-progress) + self.goal * progress
        self.widget.queue_draw()
        return progress < 1


class Workspace:
    def __init__(self, active: bool, empty: bool):
        self.active = active
        self.empty = empty

    def __repr__(self):
        return f"Workspace({self.active},{self.empty})"


class Workspaces(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()
        self.set_draw_func(self.on_draw)
        self.set_size_request(
            (WORKSPACE_SPACING + WORKSPACE_SIZE * 2) * WORKSPACE_COUNT
            + WORKSPACE_SPACING,
            -1,
        )

        active_id = Hyprland.active_workspace().id
        self.active_animation = Animation(
            self,
            datetime.timedelta(milliseconds=100),
            value=(active_id-1) * (WORKSPACE_SPACING + WORKSPACE_SIZE * 2) + WORKSPACE_SPACING + WORKSPACE_SIZE,
        )

        hyprland = Hyprland.instance()
        hyprland.connect("workspacev2", self.on_workspace)
        hyprland.connect("createworkspacev2", self.on_create_workspace)
        hyprland.connect("destroyworkspacev2", self.on_destroy_workspace)

    def on_workspace(self, hyprland: Hyprland, id: str, name: str):
        self.active_animation.animate(
            (int(id)-1) * (WORKSPACE_SPACING + WORKSPACE_SIZE * 2) + WORKSPACE_SPACING + WORKSPACE_SIZE,
        )

    def on_create_workspace(self, hyprland: Hyprland, id: str, name: str):
        pass

    def on_destroy_workspace(self, hyprland: Hyprland, id: str, name: str):
        pass

    def on_draw(self, _, context: Context, width: int, height: int):
        # context.rectangle(0, 0, width, height)
        # context.set_source_rgb(1, 0, 0)
        # context.fill()

        y = height / 2

        context.new_path()
        context.arc(self.active_animation.value, y, WORKSPACE_SIZE, 0, math.pi * 2)
        context.set_source_rgb(0, 1, 0)
        context.fill()

        x = WORKSPACE_SIZE + WORKSPACE_SPACING
        for i in range(1, WORKSPACE_COUNT + 1):

            context.new_path()
            context.select_font_face("Arial")
            context.set_font_size(18)
            context.set_source_rgb(1, 1, 1)
            text_extends = context.text_extents(str(i))
            context.move_to(x - text_extends.width / 2, y + text_extends.height / 2)
            context.show_text(str(i))
            context.stroke()

            x += WORKSPACE_SIZE * 2 + WORKSPACE_SPACING

        return True
