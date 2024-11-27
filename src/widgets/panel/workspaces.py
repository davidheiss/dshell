from typing import Iterable
import cairo
from cairo import Context
from gi.repository import Gtk, GLib
from services import Hyprland
import math
from datetime import timedelta
import itertools
from typing import Callable

from animation import Animation
from windows.panel import HEIGHT

WORKSPACE_COUNT = 5
WORKSPACE_INNER = 12
WORKSPACE_OUTER = 2
WORKSPACE_SIZE = WORKSPACE_INNER + WORKSPACE_OUTER
WORKSPACE_SPACING = 4


def workspace_pos(id: int | str):
    return (
        (int(id) - 1) * (WORKSPACE_SPACING + WORKSPACE_SIZE * 2)
        + WORKSPACE_SPACING
        + WORKSPACE_SIZE
    )


class Workspace:
    def __init__(
        self, widget: Gtk.DrawingArea, duration: timedelta, id: int, active: bool
    ):
        self.id = id
        self.active = active

        self.start = Animation(widget, duration, workspace_pos(id))
        self.end = Animation(widget, duration, workspace_pos(id))
        self.color = Animation(widget, duration, 1 if active else 0)
    
    def draw(self, context: cairo.Context, height: int, width: int):
        pass

class Workspaces(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()
        self.set_draw_func(self.on_draw)
        self.set_size_request(
            (WORKSPACE_SPACING + WORKSPACE_SIZE * 2) * WORKSPACE_COUNT
            + WORKSPACE_SPACING,
            -1,
        )

        duration = timedelta(
            milliseconds=150,
        )

        active_id = Hyprland.active_workspace().id
        self.active_animation = Animation(
            self,
            duration,
            workspace_pos(active_id),
        )

        workspace_ids = list(map(lambda x: x.id, Hyprland.workspaces()))
        self.workspaces = []
        for id in range(WORKSPACE_COUNT):
            self.workspaces.append(Workspace(self, duration, id, id in workspace_ids))

        hyprland = Hyprland.instance()
        hyprland.connect("workspacev2", self.on_workspace)
        hyprland.connect("createworkspacev2", self.on_create_workspace)
        hyprland.connect("destroyworkspacev2", self.on_destroy_workspace)

    def on_workspace(self, hyprland: Hyprland, id: str, name: str):
        self.active_animation.animate(workspace_pos(id))

    def on_create_workspace(self, hyprland: Hyprland, id: str, name: str):
        pass

    def on_destroy_workspace(self, hyprland: Hyprland, id: str, name: str):
        pass

    def on_draw(self, _, context: Context, width: int, height: int):
        y = height / 2
        x = WORKSPACE_SIZE + WORKSPACE_SPACING

        for i in range(1, WORKSPACE_COUNT + 1):

            context.select_font_face("Arial")
            context.set_font_size(18)
            context.set_source_rgb(1, 1, 1)
            text_extends = context.text_extents(str(i))
            context.move_to(
                x - text_extends.x_bearing - text_extends.width / 2,
                y + text_extends.height / 2,
            )
            context.show_text(str(i))
            context.fill()

            x += WORKSPACE_SIZE * 2 + WORKSPACE_SPACING

        context.arc(
            self.active_animation.value,
            y,
            WORKSPACE_INNER,
            0,
            math.pi * 2,
        )
        context.clip()

        context.rectangle(0, 0, width, height)
        context.set_source_rgb(0.6, 0.8, 1.0)
        context.fill()

        x = WORKSPACE_SIZE + WORKSPACE_SPACING
        for i in range(1, WORKSPACE_COUNT + 1):

            context.new_path()
            context.select_font_face("Arial")
            context.set_font_size(16)
            context.set_source_rgb(0, 0, 0)
            text_extends = context.text_extents(str(i))
            context.move_to(
                x - text_extends.x_bearing - text_extends.width / 2,
                y + text_extends.height / 2,
            )
            context.show_text(str(i))
            context.fill()

            x += WORKSPACE_SIZE * 2 + WORKSPACE_SPACING

        return True
