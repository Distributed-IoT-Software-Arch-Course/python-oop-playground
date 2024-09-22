import time
import json
from random import random
from .sensor import Sensor


class TemperatureSensor(Sensor):
    """ Temperature sensor class, extends Sensor class implementing get_status method """

    def __init__(self, device_id, initial_temperature=20):
        """ Initialize the temperature sensor with a devices ID and an initial temperature """
        super().__init__(device_id, "TemperatureSensor", "Acme Inc.")

        # Initialize the temperature measurement
        self.value = initial_temperature

        # Set the timestamp of the last measurement in milliseconds
        self.timestamp = int(time.time() * 1000)

    def update_measurement(self):
        """ Update the temperature measurement of the sensor in a range of 20 to 30 degrees with a random increment """

        # Update the temperature measurement with a random increment or decrement
        is_increment_decrement = random() > 0.5

        if is_increment_decrement:
            self.value -= random() - 0.5
        else:
            self.value += random() - 0.5

        # Set the timestamp of the last measurement in milliseconds
        self.timestamp = int(time.time() * 1000)

    def get_json_description(self):
        """ Returns a JSON representation of the temperature sensor """
        result_dict = {
            "device_id": self.device_id,
            "device_type": self.device_type,
            "device_manufacturer": self.device_manufacturer,
            "value": self.value,
            "timestamp": self.timestamp
        }

        return json.dumps(result_dict)