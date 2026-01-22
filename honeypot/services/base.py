from abc import ABC, abstractmethod

class BaseService(ABC):
    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    async def start(self):
        pass
