from abc import ABC, abstractmethod

from pypura import enums
from pypura import helpers

class BaseSensor(ABC):

    def __init__(self, device, data):
        self._device = device
        self._attr = data

    def update(self, data):
        for k,v in data.items():
            if k in self._attr:
                if type(self._attr[k]) == type(enums.DiffuserSide.LEFT):
                    self._attr[k] = enums.DiffuserSide(v)
                else:
                    self._attr[k] = v

    @property
    def type(self):
        return self.__class__.__name__

    @abstractmethod
    def to_json(self):
        pass