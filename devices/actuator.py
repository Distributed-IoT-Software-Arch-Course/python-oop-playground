from .device import Device


class Actuator(Device):
    """ Base class for actuators """

    def __init__(self, device_id, device_type, device_manufacturer):
        """ Initialize the actuator with a devices ID and a devices type """
        super().__init__(device_id, device_type, device_manufacturer)

        # Initialize the status to None, subclasses should set the status when needed
        self.status = "off"

        # Set the timestamp to None, subclasses should set the timestamp when updating the status
        self.timestamp = None

    def invoke_action(self, action_type, payload):
        """ Invoke an action on the actuator """
        raise NotImplementedError("This method should be overridden by subclasses")

    def get_json_description(self):
        """ Returns a JSON representation of the actuator,this method should be overridden by subclasses """
        raise NotImplementedError("This method should be overridden by subclasses")