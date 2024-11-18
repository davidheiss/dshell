from typing import Iterable
import cairo
from cairo import Context
from gi.repository import Gtk, GLib
from services import Hyprland
from enum import Enum
import math
import datetime
import itertools

from windows.panel import HEIGHT

WORKSPACE_COUNT = 5
WORKSPACE_SIZE = 14
WORKSPACE_SPACING = 4


def easeInSine(x: float):
    return 1 - math.cos(x * math.pi / 2)


def easeInOutBack(x: float):
    c1 = 1.70158
    c2 = c1 * 1.525

    return (
        (math.pow(2 * x, 2) * ((c2 + 1) * 2 * x - c2)) / 2
        if x < 0.5
        else (math.pow(2 * x - 2, 2) * ((c2 + 1) * (x * 2 - 2) + c2) + 2) / 2
    )


class Animation:
    def __init__(
        self,
        widget: Gtk.DrawingArea,
        duration: datetime.timedelta,
        value: float = 0,
        timing=easeInSine,
    ):
        self.widget = widget
        self.duration = duration
        self.start = value
        self.goal = value
        self.value = value
        self.id = None
        self.time = None
        self.timing = timing

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
        self.value = self.start * (1 - self.timing(progress)) + self.goal * self.timing(
            progress
        )
        self.widget.queue_draw()
        return progress < 1


class Group(set[int]):
    def __init__(self, ids: Iterable[int]):
        super().__init__(ids)
        pass

    def __contains__(self, key: int):
        return min(self) - 1 <= key <= max(self) + 1 if len(self) > 0 else False

    def can_split(self):
        for i,j in itertools.pairwise(self):
            if i + 1 != j:
                return True
        return False

    def split(self):
        return Groups(self)


    def draw(self, context: cairo.Context, width, height):
        if len(self) == 0:
            return

        start = workspace_pos(min(self))
        end = workspace_pos(max(self))
        y = height / 2

        context.arc(start, y, WORKSPACE_SIZE, math.pi * 0.5, math.pi * 1.5)
        context.arc(end, y, WORKSPACE_SIZE, math.pi * 1.5, math.pi * 0.5)
        context.set_source_rgb(0.4, 0.6, 0.8)
        context.fill()

class Groups(list[Group]):
    def __init__(self, iterable: Iterable[int]):
        super().__init__()
        for id in iterable:
            for group in self:
                if id in group:
                    group.add(id)
                    break
            else:
                self.append(Group([id]))

    def create(self, widget: Gtk.DrawingArea, id: int | str):
        widget.queue_draw()

    def destory(self, widget: Gtk.DrawingArea, id: int | str):
        widget.queue_draw()

def workspace_pos(id: int | str):
    return (
        (int(id) - 1) * (WORKSPACE_SPACING + WORKSPACE_SIZE * 2)
        + WORKSPACE_SPACING
        + WORKSPACE_SIZE
    )


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
            datetime.timedelta(milliseconds=150),
            value=(active_id - 1) * (WORKSPACE_SPACING + WORKSPACE_SIZE * 2)
            + WORKSPACE_SPACING
            + WORKSPACE_SIZE,
        )

        workspace_ids = list(map(lambda x: x.id, Hyprland.workspaces()))
        self.groups = Groups(workspace_ids)

        hyprland = Hyprland.instance()
        hyprland.connect("workspacev2", self.on_workspace)
        hyprland.connect("createworkspacev2", self.on_create_workspace)
        hyprland.connect("destroyworkspacev2", self.on_destroy_workspace)

    def on_workspace(self, hyprland: Hyprland, id: str, name: str):
        self.active_animation.animate(workspace_pos(id))

    def on_create_workspace(self, hyprland: Hyprland, id: str, name: str):
        self.groups.create(self, id)

    def on_destroy_workspace(self, hyprland: Hyprland, id: str, name: str):
        self.groups.destory(self, id)

    def on_draw(self, _, context: Context, width: int, height: int):
        y = height / 2

        for group in self.groups:
            group.draw(context, width, height)

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
            WORKSPACE_SIZE,
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
