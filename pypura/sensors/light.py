from .base_sensor import BaseSensor

from pypura import const
from pypura import urls

class Light(BaseSensor):
    def __init__(self, device, doc):
        super().__init__(device, doc)

    def turn_on(self, brightness):
        self.brightness = self._brightness_value(brightness)
        if self.brightness == 0:
            self.turn_off()
            return

        self.on = True        
        self._device.send_request()
    
    def turn_off(self):
        self.on = False
        self._device.send_request()

    def set_color(self, color, brightness):
        self.color = color
        self.brightness = self._brightness_value(brightness)

        if self.color == const.RGB_BLACK:
            self.turn_off()
            return
        
        if self.brightness == 0:
            self.turn_off()
            return
        
        self.on = True        
        self._device.send_request()

    def _brightness_value(self, val):
        if val < 0:
            return 0
        if val > 100:
            return 100
        
        return val
    
    @property
    def on(self):
        return self._attr['on']
    
    @on.setter
    def on(self, val: bool):
        self._attr['on'] = val
    
    @property
    def brightness(self):
        return self._attr['brightness']
    
    @brightness.setter
    def brightness(self, val: int):
        self._attr['brightness'] = val

    @property
    def color(self):
        return self._attr['color']
    
    @color.setter
    def color(self, val):
        self._attr['color'] = val

    @property
    def _form_data(self):
        return { 'light' : { 'on' : self.on, 'brightness' : self.brightness, 'color' : self.color } }
    
    def to_json(self):
        j = {}
        j['__type__'] = self.type
        j['on'] = self.on
        j['color'] = self.color
        j['brightness'] = self.brightness

        return j