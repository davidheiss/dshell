from .service import Service

class Services(dict):
    def __getitem__(self, key: Service):
        service = self.get(key)
        if service is None:
            service = self[key] = key()
        return service
        