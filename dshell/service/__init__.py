from .service import Service
from .manager import Manager
from .hyprerland import Hyprland
from .datetime import DateTime
from .battery import Battery

__all__ = [
    "Service",
    "Manager",
    "Hyprland",
    "DateTime",
    "Battery",
    "get_service",
]


def get_service[T: Service](service: type[T]):
    from ..app import App

    return App.instance().services.get(service)
