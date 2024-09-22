from .device import Device


class Sensor(Device):
    """ Base class for sensors """

    def __init__(self, device_id, device_type, device_manufacturer):
        """ Initialize the sensor with a devices ID, a devices type """
        super().__init__(device_id, device_type, device_manufacturer)

        # Initialize the measurement value to None and the timestamp
        # Subclasses should override the update_measurement method to set the value
        self.value = None

        # Set the timestamp to None, subclasses should set the timestamp when updating the measurement
        self.timestamp = None

    def update_measurement(self):
        """ Update the measurement of the sensor, this method should be overridden by subclasses """
        raise NotImplementedError("This method should be overridden by subclasses")

    def get_json_description(self):
        """ Returns a JSON representation of the Sensor, this method should be overridden by subclasses """
        raise NotImplementedError("This method should be overridden by subclasses")