from data.data_manager import DataManager
from home.smart_home import SmartHome
from devices.sensor import Sensor
from devices.actuator import Actuator
from devices.temperature_sensor import TemperatureSensor
from devices.humidity_sensor import HumiditySensor
from devices.smart_light import SmartLight


# Main function to test the smart home
if __name__ == '__main__':

    # Create the smart home
    my_smart_home = SmartHome(DataManager(), "SH001", 37.7749, -122.4194)

    # Add devices
    temp_sensor = TemperatureSensor(device_id=1)
    humidity_sensor = HumiditySensor(device_id=2)
    smart_light = SmartLight(device_id=3)

    my_smart_home.add_device(temp_sensor)
    my_smart_home.add_device(humidity_sensor)
    my_smart_home.add_device(smart_light)

    # Get Initial Status of all devices
    print("\nInitial Status of IoT Devices:")
    for device in my_smart_home.get_all_devices():
        # Check if the devices is a sensor or an actuator and print the value or the status
        if isinstance(device, Sensor):
            print(f'Sensor: {device.device_id} Value: {device.value} Timestamp: {device.timestamp}')
        elif isinstance(device, Actuator):
            print(f'Actuator: {device.device_id} Value: {device.status} Timestamp: {device.timestamp}')

    # Monitor the smart home for 5 seconds
    my_smart_home.monitor_home(seconds=5)

    # Get all stored measurements
    measurements = my_smart_home.get_all_measurements()
    print("\nStored Measurements:")
    for device_id, device_measurements in measurements.items():
        for measurement in device_measurements:
            print(f"Device {device_id} - Measurement: {measurement}")

    # Print Json Description of all devices
    print("\nJson Description of all devices:")
    for device in my_smart_home.get_all_devices():
        print(device.get_json_description())