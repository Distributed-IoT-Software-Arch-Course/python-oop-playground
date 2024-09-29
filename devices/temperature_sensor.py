import time
from random import random
from .sensor import Sensor


class TemperatureSensor(Sensor):
    """ Temperature sensor class, extends Sensor class implementing get_status method """

    CELSIUS_UNIT = "C"

    def __init__(self, device_id, initial_temperature=20):
        """ Initialize the temperature sensor with a devices ID and an initial temperature """
        super().__init__(device_id, "TemperatureSensor", "Acme Inc.")

        # Initialize the temperature measurement
        self.value = initial_temperature

        # Set the timestamp of the last measurement in milliseconds
        self.timestamp = int(time.time() * 1000)

        # Set the Temperature Sensor Unit to Celsius
        self.unit = TemperatureSensor.CELSIUS_UNIT

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