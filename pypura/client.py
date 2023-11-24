import functools
import json

from more_itertools import consume
from requests_toolbelt import sessions

from pypura.device import PuraDevice
from pypura import mock
from pypura import urls

class Client:

    def __init__(self, host : str, refresh : bool = False):
        self._host = host
        self._devices = None
        self._session = sessions.BaseUrlSession(host)

        if refresh:
            self.get_devices()

    def get_devices(self, refresh: bool = False):
        if refresh or self._devices is None:
            self.update_devices()

        return [
            device
            for device in self._devices.values()
        ]
    
    def get_device(self, device_id, refresh : bool = False):
        if refresh or self._devices is None:
            self.update_device(device_id)

        return self._devices.get(device_id)
    
    def update_devices(self):
        self._load_devices()

    def update_device(self, device_id):
        url = urls.DEVICE.format(id = device_id)
        response = self.send_request("get", url)
        response = response.json()['data']['device_info']
        self._load_device(response)

    def send_request(self, method, path, headers=None, data=None):
        response = getattr(self._session, method)(path, headers=headers, json=data, verify=False)

        #if response and response.status_code < 400:
        return response
    
    def _load_devices(self):
        if self._devices is None:
            self._devices = {}

        response = self.send_request("get", urls.DEVICES)
        if response.status_code == 200:
            devices = response.json()['data']
            consume(map(self._load_device, devices))
        else:
            raise Exception("error loading devices")
       
    def _load_device(self, doc_str):
        if self._devices is None:
            self._devices = {}

        doc = json.loads(doc_str)
        self._reuse_device(doc) or self._create_new_device(doc)

    def _reuse_device(self, doc):
        device = self._devices.get(doc['id'])

        if not device:
            return

        device.update(doc)
        return device

    def _create_new_device(self, doc):
        device = PuraDevice(self, doc)

        if not device:
            return

        self._devices[device.id] = device


