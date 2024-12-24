import math
from datetime import timedelta

from gi.repository import Gtk, Gdk  # type: ignore
import cairo

from ..animation import Animation, Color
from ..service import get_service, Hyprland

COUNT = 5
SIZE_DEFAULT = 10
SIZE_ACTIVE = 12
WIDTH_DEFAULT = 0
WIDTH_ACTIVE = 8
SPACING = 3

DURATION = timedelta(milliseconds=150)

COLOR_DEFAULT = Color(1, 1, 1) * 0.33
COLOR_CREATED = Color(1, 1, 1) * 0.66
COLOR_ACTIVE = Color(1, 1, 1)


class _Workspace:
    def __init__(self, widget: Gtk.Widget, id, active: bool, created: bool):
        self.id = id
        self.active = active
        self.created = created

        if active:
            self.size = Animation(SIZE_ACTIVE, widget, DURATION)
            self.color = Animation(COLOR_ACTIVE, widget, DURATION)
            self.width = Animation(WIDTH_ACTIVE, widget, DURATION)
        else:
            self.size = Animation(SIZE_DEFAULT, widget, DURATION)
            self.width = Animation(WIDTH_DEFAULT, widget, DURATION)
            if created:
                self.color = Animation(COLOR_CREATED, widget, DURATION)
            else:
                self.color = Animation(COLOR_DEFAULT, widget, DURATION)

    def activate(self):
        self.active = True
        self.color.to(COLOR_ACTIVE)
        self.size.to(SIZE_ACTIVE)
        self.width.to(WIDTH_ACTIVE)

    def deactivate(self):
        self.active = False
        if self.created:
            self.color.to(COLOR_CREATED)
        else:
            self.color.to(COLOR_DEFAULT)
        self.size.to(SIZE_DEFAULT)
        self.width.to(WIDTH_DEFAULT)

    def create(self):
        self.created = True

    def destroy(self):
        self.created = False
        self.color.to(COLOR_DEFAULT)
        self.size.to(SIZE_DEFAULT)
        self.width.to(WIDTH_DEFAULT)

    def __repr__(self):
        return str((self.id, self.active, self.created))


class WorkspaceDrawing(Gtk.DrawingArea):
    def __init__(self):
        super().__init__(
            width_request=(SIZE_DEFAULT + SPACING + WIDTH_DEFAULT) * (COUNT)
            - SPACING
            + SIZE_ACTIVE
            - SIZE_DEFAULT
            + WIDTH_ACTIVE,
            height_request=SIZE_ACTIVE,
        )

        self.set_draw_func(self.do_draw)

        active = int(Hyprland.command("activeworkspace")["id"])
        created = list(map(lambda x: int(x["id"]), Hyprland.command("workspaces")))
        self.workspaces = [
            _Workspace(self, id, id == active, id in created)
            for id in range(1, COUNT + 1)
        ]
        self.index = active - 1

        hyprland = get_service(Hyprland)
        hyprland.connect("workspacev2", self.do_workspacev2)
        hyprland.connect("createworkspacev2", self.do_createworkspacev2)
        hyprland.connect("destroyworkspacev2", self.do_destroyworkspacev2)

    def do_createworkspacev2(self, service: Hyprland, id: str, name: str):
        index = int(id) - 1
        self.workspaces[index].create()

    def do_destroyworkspacev2(self, service: Hyprland, id: str, name: str):
        index = int(id) - 1
        self.workspaces[index].destroy()

    def do_workspacev2(self, service: Hyprland, id: str, name: str):
        self.workspaces[self.index].deactivate()
        index = int(id) - 1
        self.workspaces[index].activate()
        self.index = index

    def do_draw(self, _, context: cairo.Context, width: int, height: int):
        
        size = sum(map(lambda x: x.size.value + x.width.value, self.workspaces)) + SPACING * (len(self.workspaces)-1)
        missing = width - size

        x = 0
        y = height / 2
        for workspace in self.workspaces:
            size = workspace.size.value
            width = workspace.width.value
            if workspace.active:
                width += missing
            context.arc(x + size / 2, y, size / 2, math.pi * 1 / 2, math.pi * 3 / 2)
            context.arc(
                x + size / 2 + width, y, size / 2, math.pi * 3 / 2, math.pi * 1 / 2
            )
            context.set_source_rgb(*workspace.color.value)
            context.fill()
            x += size + width + SPACING

class Workspace(Gtk.Button):
    def __init__(self):
        super().__init__(
            css_classes=["workspace"],
            child=WorkspaceDrawing(),
            valign=Gtk.Align.CENTER,
            cursor=Gdk.Cursor.new_from_name("pointer")
        )
    
    def do_clicked(self):
        print("clicked")
