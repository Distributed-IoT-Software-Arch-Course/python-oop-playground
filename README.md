# Python Object-Oriented Programming Playground

This is a playground for Python Object Oriented Programming (OOP) concepts. 
The goal is to provide a hands-on experience with OOP concepts in Python.

The proposed modeling is associated to a Smart Home with various IoT devices: 

- Temperature sensors
- Humidity sensors
- Smart lights

The exercise will involve designing data structure, identify classes (and creating them in Python to model these devices, 
a central system to collect and manage data.

**Note:** The scenario is simplified without any kind of communication, and everything is running within the same process. 

## Base Classes

The basic classes are:

- `Device`: Base class for all devices defining the following attributes for all the devices such as sensors and actuators subclasses:
  - `device_id`: Id of the device
  - `device_type`: Type of the device
  - `device_manufacturer`: Manufacturer of the device
- `Sensor`: Base class for all sensors extending `Device` class and adding: 
  - Methods:
    - `update_measurement()`: update the sensor value. The default implementation throws a `NotImplementedError` exception and the subclasses must implement it. 
    - `get_json_description()`: get the description of the sensor in JSON format. The default implementation throws a `NotImplementedError` exception and the subclasses must implement it.
  - Attributes:
    - `value`: associated to the current sensor value
    - `unit`: mapping the unit associated to the physical measurement type
    - `timestamp` of the last sample in milliseconds
- `Actuator`: Base class for all actuators extending `Device` class and adding:
  - Methods:
    - `invoke_action(action_type, payload)`: method and the `get_json_description` method to get the description of the sensor in JSON format
    - `get_json_description()`: get the description of the sensor in JSON format. The default implementation throws a `NotImplementedError` exception and the subclasses must implement it.
  - Attributes:
    -  `status`: associated to the current status of the actuator
    - `timestamp` of the last action in milliseconds

## Sensors & Actuator Classes

Starting from the base classes, we have the following subclasses:

- `TemperatureSensor`: A sensor that measures temperature extending `Sensor` class and mapping a default initial value of 20.0, unit of Celsius, a timestamp of the last sample in milliseconds.
   , the random value is generated between 20 and 30 degrees with a random increment between -0.5 to 0.5 degrees.
- `HumiditySensor`: A sensor that measures humidity extending `Sensor` class and mapping a default initial value of 50.0, unit of percentage, a timestamp of the last sample in milliseconds.
   , the random value is generated between 40% and 60% percentage with a random increment between -5% to 5%.
- `SmartLight`: An actuator that can be turned on or off extending `Actuator` class and mapping a default initial status of `OFF`, a timestamp of the last action in milliseconds. The `invoke_action(action_type, payload)`
   method check the received action type and if it supported (`SWITCH` value) together with the correct value of the payload (`ON` or `OFF`) change the current value of the actuator and align the associated timestamp.

## Data Management

The class `DataManager` has been defined to shape how data are managed in the application, to centralize the associated methods and 
_hide_ how data and information are effectively stored by the class itself.

The actual implementation has the following main capabilities:

- **Device Management**: allows to store and retrieve Devices for the Smart Home through dedicated method. The adopted data structure is a `list` of devices.
- **Measurement Management**: supports the saving and retrieval of sensor measurements and actuator variations over time.

Implemented and supported methods are:

- `add_device(device)`: Add a new device to the Data Manager
- `remove_device(device_id)`: Remove a device from the Data Manager 
- `get_device(device_id)`: Get a device by its Id from the stored devices on the Data Manager
- `store_measurement(device_id, measurement)`: Store a measurement for a device. It can be associated both a variation of a Sensor or a status change in an actuator
- `get_measurements(device_id)`: Get all measurements for a specific device
- `get_all_measurements()`: Retrieve all the stored measurements

## Smart Home

The Smart Home class is in charge of two main responsibilities: 

- **Device Management**: Exposes the capabilities to manage devices (`add`, `remove`, and `get`) hiding the fact that it is using an instance of the `DataManager` to do that.
- **Measurement Service**: Exposes stored measurements associated to both sensors and actuators hiding the fact that it is using an instance of the `DataManager` to do that.
- **Home Monitoring**: Implements a method to emulate the `monitoring` of the Smart Home that periodically check and update sensors measurements and randomly change actuators status.

## Main Application

The `main.py` file is the entry point of the application. It creates a Smart Home instance and adds some devices to it.
It also starts the monitoring of the Smart Home and prints the measurements of the devices.

```python
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
```

## File Organization & Modules

To organize your classes and files into different folders, you can follow these steps:  
Create a Directory Structure: Organize your files into directories based on their functionality. For example:  

```text
smart_home_project/
├── data
    ├── __init__.py
    ├── data_manager.py
├── devices/
│   ├── __init__.py
│   ├── actuator.py
│   ├── sensor.py
│   ├── smart_light.py
├── main.py
├── smart_home.py
└── README.md
```
The `__init__.py` file is used to mark a directory as a Python package. 
This allows you to import modules from that directory. 
Here are the main reasons why you need an `__init__.py` file:  

- **Package Initialization:** It can be used to execute initialization code for the package or set the __all__ variable to control what is imported when from package import * is used.  
- **Namespace Management:** It helps in managing the namespace of the package, ensuring that the modules within the package can be imported correctly.  
- **Compatibility:** In older versions of Python (before 3.3), the presence of __init__.py was required to recognize a directory as a package. Although it is not strictly necessary in Python 3.3 and later, it is still a good practice to include it for compatibility and clarity.

After that you have to update imports adjusting the import statements in your files to reflect the new directory structure.
For example in the `main.py` we will have an updated import for SmartLight class:

```python
from data.data_manager import DataManager
from home.smart_home import SmartHome
from devices.smart_light import SmartLight

[...]
```

If you have an import from a different class within the same directory you should use a relative import
like the following statement: 

```python
from .device import Device
```