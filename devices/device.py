import json

class Device:
    """ Base class for devices """

    def __init__(self, device_id, device_type, device_manufacturer):
        """ Initialize the devices with a devices ID and a devices type """
        self.device_id = device_id
        self.device_type = device_type
        self.device_manufacturer = device_manufacturer

    def get_json_measurement(self):
        """ Returns a JSON representation of the Status of the device (e.g., the last measurement) """
        raise NotImplementedError("This method should be overridden by subclasses")

    def get_json_description(self):
        """ Returns a JSON representation of the Device """

        result_dict = {
            "device_id": self.device_id,
            "device_type": self.device_type,
            "device_manufacturer": self.device_manufacturer
        }

        return json.dumps(result_dict)
