from .service import Service
from .services import Services
from .hyprerland import HyprlandService
from .datetime import DateTimeService
from .battery import BatteryService

__all__ = [
    "Service",
    "Services",
    "HyprlandService",
    "DateTimeService",
    "BatteryService",
    "get_service",
]


def get_service[T: Service](service: type[T]) -> T:
    from ..app import App

    return App.instance().service_manager[service]
