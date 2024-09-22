import time
import json
from .sensor import Sensor
from random import random


class HumiditySensor(Sensor):
    """ Humidity sensor class, extends Sensor class implementing required methods defined in the Sensor Class """

    # Relative Humidity % Unit
    HUMIDITY_UNIT = "%RH"

    def __init__(self, device_id, initial_humidity=50):
        """ Initialize the humidity sensor with a devices ID and an initial humidity level """
        super().__init__(device_id, "HumiditySensor", "Acme Inc.")

        # Initialize the humidity measurement
        self.value = initial_humidity

        # Set the timestamp of the last measurement in milliseconds
        self.timestamp = int(time.time() * 1000)

        # Set Humidity Unit to Relative Humidity % Unit
        self.unit = HumiditySensor.HUMIDITY_UNIT

    def update_measurement(self):
        """ Update the humidity measurement of the sensor in a range of 40% to 60% with a random increment """

        # Update the humidity measurement with a random increment or decrement
        is_increment_decrement = random() > 0.5

        if is_increment_decrement:
            self.value += 10 * (random() + 0.5)
        else:
            self.value -= 10 * (random() + 0.5)


        # Set the timestamp of the last measurement in milliseconds
        self.timestamp = int(time.time() * 1000)

    def get_json_description(self):
        """ Returns a JSON representation of the humidity sensor """
        result_dict = {
            "device_id": self.device_id,
            "device_type": self.device_type,
            "device_manufacturer": self.device_manufacturer,
            "value": self.value,
            "unit": self.unit,
            "timestamp": self.timestamp
        }

        return json.dumps(result_dict)