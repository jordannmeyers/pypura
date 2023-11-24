import json

from more_itertools import consume

from pypura.sensors.light import Light
from pypura.sensors.diffuser import Diffuser
from pypura import enums
from pypura import helpers
from pypura import const
from pypura import urls

class PuraDevice:

    def __init__(self, client, data):
        self.client = client

        self._load_info(data)
        self._load_sensors(data)

    def turn_light_on(self, brightness : int = 100):
        self._sensors['light'].turn_on(brightness)

    def turn_light_off(self):
        self._sensors['light'].turn_off()

    def set_light_color(self, color, brightness : int = 100):
        self._sensors['light'].set_color(color, brightness)

    def turn_diffuser_on(self, side, intensity : int = 4):
        if type(side) == type(int):
            side = enums.DiffuserSide(side)

        if side == enums.DiffuserSide.LEFT:
            self._sensors['diffuser_right'].on = False
            self._sensors['diffuser_left'].turn_on(intensity)
        elif side == enums.DiffuserSide.RIGHT:
            self._sensors['diffuser_left'].on = False
            self._sensors['diffuser_right'].turn_on(intensity)
        else:
            raise Exception()
        
    def turn_diffuser_off(self):
        self._sensors['diffuser_left'].on = False
        self._sensors['diffuser_right'].on = False
        if not self._sensors['light'].on:
            self._sensors['light'].turn_off()
        else:
            self._sensors['light'].set_color(self._sensors['light'].color, self._sensors['light'].brightness)

    def swap_scent(self, side, code):
        diffuser_str = None
        if side == enums.DiffuserSide.LEFT:
            diffuser_str = 'left'
        elif side == enums.DiffuserSide.RIGHT:
            diffuser_str = 'right'
        else:
            raise Exception()     
        
        data = { 'side' : diffuser_str, 'code' : code }
        url = urls.SWAP_SCENT.format(id = self.id)
        respo = self.client.send_request('put', url, data=data)

        k = 0

    def update(self, data):
        self._sensors['light'].update(data['light'])

        self._sensors['diffuser_left'].update(data['diffuser_left'])
        self._sensors['diffuser_right'].update(data['diffuser_right'])

    def send_request(self):
        req_json = {}
        req_json.update(self._sensors['light']._form_data)

        req_json.update(self._sensors['diffuser_left']._form_data)
        req_json.update(self._sensors['diffuser_right']._form_data)

        self.client.send_request('put', self._device_url, data=req_json)
        
    @property
    def id(self):
        return self._attr['id']

    @property
    def manufacturer(self):
        return self._attr['manufacturer']
    
    @property
    def model(self):
        return self._attr['model']
    
    @property
    def name(self):
        return self._attr['name']
    
    @name.setter
    def name(self, val: str):
        self._attr['name'] = val

    @property
    def connected(self):
        return self._attr['connected']
    
    @connected.setter
    def connected(self, val: bool):
        self._attr['connected'] = val

    @property
    def _device_url(self):
        return urls.DEVICE.format(id = self.id)

    def _load_info(self, data):
        self._attr = {}

        self._attr['id'] = data['id']
        self._attr['connected'] = self._get_info_or_default(data, 'connected', False)
        self._attr['name'] = self._get_info_or_default(data, 'name', self._attr['id'])
        self._attr['manufacturer'] = self._get_info_or_default(data, 'manufacturer', const.DEFAULT_MANUFACTURER)
        self._attr['model'] = self._get_info_or_default(data, 'model', const.DEFAULT_MODEL)
            
    def _get_info_or_default(self, data, attr_name, default_value):
        if attr_name in data:
            return data[attr_name]
        else:
            return default_value

    def _load_sensors(self, data):
        self._sensors = {}

        # light
        self._sensors['light'] = Light(self, data['light'])

        # diffusers
        self._sensors['diffuser_left'] = Diffuser(enums.DiffuserSide.LEFT, self, data['diffuser_left'])
        self._sensors['diffuser_right'] = Diffuser(enums.DiffuserSide.RIGHT, self, data['diffuser_right'])
                   
    def to_json(self):
        j = {}
        j['__type__'] = self.__class__.__name__
        j['id'] = self.id
        j['connected'] = self.connected
        j['name'] = self.name
        j['manufacturer'] = self.manufacturer
        j['model'] = self.model
        j['light'] = self._sensors['light'].to_json()
        j['diffuser_left'] = self._sensors['diffuser_left'].to_json()
        j['diffuser_right'] = self._sensors['diffuser_right'].to_json()

        return j