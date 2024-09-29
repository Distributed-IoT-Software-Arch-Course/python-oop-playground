from .actuator import Actuator
import time

class SmartLight(Actuator):
    """ Class representing a smart light devices """

    # Static Class's attributes used to define action types and values
    STATUS_ON = "ON"
    STATUS_OFF = "OFF"
    ACTION_TYPE_SWITCH = "SWITCH"

    def __init__(self, device_id):
        """ Initialize the smart light with a devices ID and an initial state """
        super().__init__(device_id, "SmartLight", "Acme Inc.")

        # Set the initial state of the smart light to off
        self.status = SmartLight.STATUS_OFF

        # Set the timestamp to None, subclasses should set the timestamp when updating the status
        self.timestamp = int(time.time() * 1000)

    def invoke_action(self, action_type, payload):
        """ Invoke an action on the smart light """

        # Check if action_type Type and payload are Strings
        if not isinstance(action_type, str) or not isinstance(payload, str):
            raise ValueError("Action type and payload must be strings")

        # Check the action type and payload
        if action_type.upper() == SmartLight.ACTION_TYPE_SWITCH and payload.upper() in [SmartLight.STATUS_ON, SmartLight.STATUS_OFF]:
            self.status = payload
        else:
            raise ValueError("Unsupported action type")