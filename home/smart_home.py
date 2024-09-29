import time
from random import random

from devices.device import Device
from devices.sensor import Sensor
from devices.smart_light import SmartLight


class SmartHome:
    """ Smart home class that manages devices and data """

    def __init__(self, storage_manager, home_id, latitude, longitude):
        """Initialize the smart home with an empty list of devices and a data manager """
        self.data_manager = storage_manager
        self.home_id = home_id
        self.latitude = latitude
        self.longitude = longitude

        # Initialize the internal structure for managing device references
        self.device_dict = {}

    def add_device(self, device):
        """ Add a new devices to the smart home """

        # If the Class type is correct
        if isinstance(device, Device):
            # Add the Device to the internal structure
            self.device_dict[device.device_id] = device

            # Save the Device Description through the Data Manager
            self.data_manager.store_device_description(device.device_id, device.get_json_description())
        else:
            raise TypeError("Expected Device Class ! Error a different type has been provided !")


    def remove_device(self, device_id):
        """ Remove a devices from the smart home """

        if device_id in self.device_dict.keys():
            ## Remove the device from the internal structure and from the storage
            del self.device_dict[device_id]
            self.data_manager.remove_device_description(device_id)
        else:
            print(f'Warning ! Device with Id: {device_id} not found ... nothing to remove')

    def get_device(self, device_id):
        """ Get a devices by its ID """
        if device_id in self.device_dict.keys():
            return self.device_dict[device_id]
        else:
            return None

    def get_all_devices(self):
        """ Get all devices in the smart home """
        return self.device_dict

    def get_all_device_descriptions(self):
        """ Return all the stored Device Descriptions """
        return self.data_manager.get_all_device_descriptions()

    def get_all_measurements(self):
        """ Get all measurements for all devices """
        return self.data_manager.get_all_measurements()

    def monitor_home(self, seconds=5):
        """ Monitor the smart home for a given number of seconds """

        # Iterate 5 times over the list of devices and update the measurements or trigger actions every 2 seconds
        for _ in range(seconds):
            # Wait for 2 seconds
            print("\nWaiting for 1 seconds...")
            time.sleep(1)

            for device in self.get_all_devices().values():

                # Here we can check if the devices is a sensor and update the measurement with Sensor base class
                if isinstance(device, Sensor):
                    print(f"Updating measurement for devices {device.device_id} ...")
                    device.update_measurement()
                    self.data_manager.store_measurement(device.device_id, device.get_json_description())

                # Here we check explicitly for the SmartLight class since the payload is different and custom
                elif isinstance(device, SmartLight):

                    # Flip a coin and decide to switch the light on or off
                    random_value = random()

                    # If random value is greater than 0.5 change the state of the light
                    if random_value > 0.5:

                        original_status = device.status

                        print(f"Changing Actuator Status: {device.device_id} ...")
                        if device.status == SmartLight.STATUS_ON:
                            device.invoke_action(SmartLight.ACTION_TYPE_SWITCH, SmartLight.STATUS_OFF)
                        else:
                            device.invoke_action(SmartLight.ACTION_TYPE_SWITCH, SmartLight.STATUS_ON)

                        new_device_status = device.status

                        print(f"Device {device.device_id} status changed from {original_status} to {new_device_status}")

                        # Store Actuation change as Measurement
                        self.data_manager.store_measurement(device.device_id, device.get_json_description())

