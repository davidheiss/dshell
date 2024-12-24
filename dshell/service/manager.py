from .service import Service

class Manager:
    def __init__(self):
        self.services: dict[type[Service], Service] = {}
    
    def get[T: Service](self, cls: type[T]) -> T:
        service = self.services.get(cls)
        if service is None:
            service = self.services[cls] = cls()
        return service