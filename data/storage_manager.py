class StorageManager:
    """ Class to manage the data storage of the smart home """

    def __init__(self):
        """ Initialize the data manager with an empty dictionary to store sensor data """
        self.device_description_dict = {}
        self.device_measurement_dict = {}

    def store_device_description(self, device_id, device_description):
        """ Store a new device description """
        self.device_description_dict[device_id] = device_description

    def remove_device_description(self, device_id):
        """ Remove a stored device description """
        if device_id in self.device_description_dict.keys():
            del self.device_measurement_dict[device_id]

    def get_device_description(self, device_id):
        """ Get a device description by its ID """
        if device_id in self.device_description_dict.keys():
                return self.device_description_dict[device_id]
        else:
            return None

    def get_all_device_descriptions(self):
        """ Return all the device Descriptions """
        return self.device_description_dict

    def store_measurement(self, device_id, measurement):
        """ Store a measurement for a devices. It can be associated both a variation of a Sensor or a status change in an actuator """
        if device_id not in self.device_measurement_dict:
            self.device_measurement_dict[device_id] = []
        self.device_measurement_dict[device_id].append(measurement)

    def get_measurements(self, device_id):
        """ Get all measurements for a specific devices """
        return self.device_measurement_dict.get(device_id, [])

    # Get all measurements for all devices
    def get_all_measurements(self):
        """ Get all measurements for all devices """
        return self.device_measurement_dict


