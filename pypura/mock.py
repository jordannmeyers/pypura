import json

def mock_device_response():
    return {
        "__type__": "Device",
        "id": "C8F09E4CBC68",
        "light": {
            "__type__": "Light",
            "on": True,
            "color": [
                255,
                0,
                0
            ],
            "brightness": 100
        },
        "diffuser_left": {
            "__type__": "Diffuser",
            "code": "HNH",
            "on": True,
            "intensity": 4,
            "runtime": 0
        },
        "diffuser_right": {
            "__type__": "Diffuser",
            "code": None,
            "on": False,
            "intensity": 4,
            "runtime": 0
        }
    }

def mock_devices_response():
    return [ mock_device_response() ]