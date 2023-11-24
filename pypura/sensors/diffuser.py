from pypura.sensors.base_sensor import BaseSensor

from pypura import const
from pypura import urls
from pypura.enums import DiffuserSide

class Diffuser(BaseSensor):
    def __init__(self, side, device, doc):
        super().__init__(device, doc)
        self.side = side
    
    def turn_on(self, intensity):
        self.on = True
        self.intensity = self._intensity_value(intensity)
        self._device.send_request()
    
    def turn_off(self):
        self.on = False
        self._device.send_request()

    def set_intensity(self, intensity):
        self.intensity = self._intensity_value(intensity)

        if self.intensity == 0:
            self.turn_off()
            return
        
        self.on = True        
        self._device.send_request()

    def _intensity_value(self, val):
        if val < 0:
            return 0
        if val > 10:
            return 10
        
        return val

    @property
    def on(self):
        return self._attr['on']
    
    @on.setter
    def on(self, val: bool):
        self._attr['on'] = val
    
    @property
    def intensity(self):
        return self._attr['intensity']
    
    @intensity.setter
    def intensity(self, val):
        self._attr['intensity'] = val

    @property
    def runtime(self):
        return self._attr['runtime']
    
    @runtime.setter
    def runtime(self, val):
        self._attr['runtime'] = val

    @property
    def code(self):
        return self._attr['code']
    
    @code.setter
    def code(self, val):
        self._attr['code'] = val
    
    @property
    def side(self):
        return self._attr['side']
    
    @side.setter
    def side(self, val):
        self._attr['side'] = val

    @property
    def _form_data(self):
        return { "{}".format({True: "diffuser_left", False: "diffuser_right"} [self.side == DiffuserSide.LEFT]) : { 'on' : self.on, 'intensity' : self.intensity } }
    
    def to_json(self):
        j = {}
        j['__type__'] = self.__class__.__name__
        j['on'] = self.on
        if isinstance(self.side, DiffuserSide):
            j['side'] = self.side.value
        else:
            j['side'] = self.side
        j['intensity'] = self.intensity
        j['runtime'] = self.runtime
        j['code'] = self.code

        return j