class DataManager:
    """ Class to manage the data of the smart home """

    def __init__(self):
        """ Initialize the data manager with an empty dictionary to store sensor data """
        self.devices = []
        self.sensor_data = {}

    def add_device(self, device):
        """ Add a new devices to the smart home """
        self.devices.append(device)

    def remove_device(self, device_id):
        """ Remove a devices from the smart home """
        for device in self.devices:
            if device.device_id == device_id:
                self.devices.remove(device)
                return

    def get_device(self, device_id):
        """ Get a devices by its ID """
        for device in self.devices:
            if device.device_id == device_id:
                return device
        return None

    def store_measurement(self, device_id, measurement):
        """ Store a measurement for a devices. It can be associated both a variation of a Sensor or a status change in an actuator """
        if device_id not in self.sensor_data:
            self.sensor_data[device_id] = []
        self.sensor_data[device_id].append(measurement)

    def get_measurements(self, device_id):
        """ Get all measurements for a specific devices """
        return self.sensor_data.get(device_id, [])

    # Get all measurements for all devices
    def get_all_measurements(self):
        """ Get all measurements for all devices """
        return self.sensor_data


