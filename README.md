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

Playground Sections:

- [JSON Introduction](#json-introduction)
- [File Organization & Modules](#file-organization--modules)
- [Base Classes](#project-base-classes)
- [Device Class](#device-class)
- [Sensor Class](#sensor-class)
- [Actuator Class](#actuator-class)
- [Sensors & Actuator SubClasses (Temperature, Humidity, SmartLight)](#sensors--actuator-subclasses)
- [Storage Management](#storage-management)
- [Smart Home](#smart-home)
- [Main Application](#main-application)
- [Managing Types in Python](#managing-types-in-python)

## Json Introduction

JSON (JavaScript Object Notation) is a lightweight data-interchange format that is easy for humans to read and write, and easy for machines to parse and generate. 
It is a text format that is completely language-independent, making it ideal for data exchange between different systems.

An example of a JSON Datastructure is:

```json
{
  "name": "John Doe",
  "age": 30,
  "city": "New York"
}
```

### Basic components of JSON

Objects:
- Enclosed in curly braces ({}).
- Contain key-value pairs separated by commas.
- Keys are strings (enclosed in double quotes).
- Values can be any valid JSON data type (including objects, arrays, strings, numbers, booleans, or null).

Arrays:
- Enclosed in square brackets ([]).
- Contain ordered lists of values separated by commas.
- Values can be any valid JSON data type.

Data types in JSON:

- Strings: Enclosed in double quotes (").
- Numbers: Can be integers or floating-point numbers.
- Booleans: true or false.
- Null: Represents the absence of a value.

Characteristics of JSON:

- Human-readable: JSON is designed to be easily read and understood by humans.
- Machine-readable: JSON is easily parsed and generated by machines.
- Lightweight: JSON is a relatively small format compared to XML.
- Language-independent: JSON is not tied to any specific programming language.
- Hierarchical: JSON data is organized in a hierarchical structure using objects and arrays.

Example of a basic JSON structure:

```json
{
  "name": "John Doe",
  "age": 30,
  "city": "New York",
  "isStudent": false,
  "hobbies": ["reading", "coding", "traveling"]
}
```

### Import Json Package

Python provides built-in support for JSON through the json module. Here's a brief overview of how to use it:

```python
import json
```

### Load JSON data from a file

This will load the JSON data from the data.json file and store it in the data variable as a Python object (e.g., dictionary, list, or a combination of both).

```python
with open('data.json', 'r') as f:
    data = json.load(f)
```

### Dump data to a JSON file

This will write the Python object data as JSON data to the output.json file.

```python
with open('output.json', 'w') as f:
    json.dump(data, f)
```

### Json & Dictionary

From Dictionary to Json String

```python
data = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

json_data = json.dumps(data)
print(json_data)
```

The output will be:

```json
{"name": "Alice", "age": 30, "city": "New York"}
```

From Json String to Dictionary

```python
json_string = '{"name": "Bob", "age": 25, "city": "Los Angeles"}'
python_dict = json.loads(json_string)

print(python_dict["name"])   # Output: Bob
print(python_dict["age"])    # Output: 25
print(python_dict["city"])   # Output: Los Angeles
```

## File Organization & Modules

To organize your classes and files into different folders, you can follow these steps:  
Create a Directory Structure: Organize your files into directories based on their functionality. For example:  

```text
smart_home_project/
├── data
    ├── __init__.py
    ├── storage_manager.py
├── devices/
│   ├── __init__.py
│   ├── actuator.py
│   ├── sensor.py
│   ├── smart_light.py
├── home/
│   ├── __init__.py
│   ├── smart_home.py
├── main.py
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
from data.storage_manager import StorageManager
from home.smart_home import SmartHome
from devices.smart_light import SmartLight

[...]
```

If you have an import from a different class within the same directory you should use a relative import
like the following statement: 

```python
from .device import Device
```

## Project Base Classes

The basic classes are:

- `Device`: Base class for all devices defining the following attributes for all the devices such as sensors and actuators subclasses:
  - `device_id`: Id of the device
  - `device_type`: Type of the device
  - `device_manufacturer`: Manufacturer of the device
  - The Device class defines two core method that will be inherited by every subclasses: 
    - `get_json_measurement`: Returns a JSON representation of the Status of the device (e.g., the last measurement o the last state of an actuator). This method should be implemented by subclasses.
    - `get_json_description`: Returns a JSON representation of the Device. The Device class already provide a default implementation that can be applied to every device and subclasses (e.g., Sensor and Actuator)
- `Sensor`: Base class for all sensors extending `Device` class and adding: 
  - Methods:
    - `update_measurement()`: update the sensor value. The default implementation throws a `NotImplementedError` exception and the subclasses must implement it. 
  - Attributes:
    - `value`: associated to the current sensor value
    - `unit`: mapping the unit associated to the physical measurement type
    - `timestamp` of the last sample in milliseconds
- `Actuator`: Base class for all actuators extending `Device` class and adding:
  - Methods:
    - `invoke_action(action_type, payload)`: method and the `get_json_description` method to get the description of the sensor in JSON format
  - Attributes:
    -  `status`: associated to the current status of the actuator
    - `timestamp` of the last action in milliseconds

## Device Class

The Device class has the following structure with a constructor to initialize the Device instance and two methods
related to Json description of the device and the associated last measurement.

```python
import json

class Device:
    """ Base class for devices """

    def __init__(self, device_id, device_type, device_manufacturer):
        """ Initialize the devices with a devices ID and a devices type """
        self.device_id = device_id
        self.device_type = device_type
        self.device_manufacturer = device_manufacturer

    def get_json_measurement(self):
        """ Returns a JSON representation of the Status of the device (e.g., the last measurement) """
        raise NotImplementedError("This method should be overridden by subclasses")

    def get_json_description(self):
        """ Returns a JSON representation of the Device """

        result_dict = {
            "device_id": self.device_id,
            "device_type": self.device_type,
            "device_manufacturer": self.device_manufacturer
        }

        return json.dumps(result_dict)
```

The method `get_json_measurement()` is not implemented since depends on the characteristics of the specific subclass
like `Sensor` that returns last measurements (e.g., Temperature) or `Actuator` that instead return the last state.

On the opposite, the method `get_json_description()` provides a default implementation describing the device in 
terms of its `id`, `type`, and `manufacturer`. This implementation is usable by every subclass but of course it can 
be overridden in order to customize or extend the behaviour.

## Sensors & Actuator Classes

The main two Subclasses for Device are `Sensor` and `Actuator` with the following structure

### Sensor Class

The `Sensor` class has the responsibility to map the properties and behaviours of the Sensors in our system and application.

```python
from .device import Device
import json

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

        # Set the Unit associated to sensor measurements
        self.unit = None
```

Then we declare and add a new method `update_measurement` in charge of structuring how each specific sensor model
the measuring of its new values. For this reason this method is empty and should be overridden by subclasses.

```python
def update_measurement(self):
    """ Update the measurement of the sensor, this method should be overridden by subclasses """
    raise NotImplementedError("This method should be overridden by subclasses")
```

On the other hand, the implementation of the `get_json_measurement` can be integrated in the `Sensor` class and then
inherited by Sensors subclasses defining how sensor measurements are reported as JSON String.

```python
def get_json_measurement(self):
    """ Returns a JSON Measurement of the humidity sensor """
    result_dict = {
        "device_id": self.device_id,
        "value": self.value,
        "unit": self.unit,
        "timestamp": self.timestamp
    }

    return json.dumps(result_dict)
```

### Actuator Class

The `Actuator` class has the responsibility to map the properties and behaviours of the Actuator in our system and application.

```python
from .device import Device
import json

class Actuator(Device):
    """ Base class for actuators """

    def __init__(self, device_id, device_type, device_manufacturer):
        """ Initialize the actuator with a devices ID and a devices type """
        super().__init__(device_id, device_type, device_manufacturer)

        # Initialize the status to None, subclasses should set the status when needed
        self.status = "off"

        # Set the timestamp to None, subclasses should set the timestamp when updating the status
        self.timestamp = None
```

With the following method `invoke_action` we model the behaviour of an Actuator that can receive and action request
and execute it starting from a `type` and a `payload` containing the detail of the action (e.g., `ON` and `OFF`).
In this case since this class is generic, this method is not implemented and should be overridden by subclasses.

```python
def invoke_action(self, action_type, payload):
    """ Invoke an action on the actuator """
    raise NotImplementedError("This method should be overridden by subclasses")
```

The 

```python
def get_json_measurement(self):
    """ Returns a JSON Measurement of the humidity sensor """
    result_dict = {
        "device_id": self.device_id,
        "status": self.status,
        "timestamp": self.timestamp
    }

    return json.dumps(result_dict)
```

## Sensors & Actuator SubClasses

Starting from the base classes, we have the following subclasses:

- `TemperatureSensor`: A sensor that measures temperature extending `Sensor` class and mapping a default initial value of 20.0, unit of Celsius, a timestamp of the last sample in milliseconds.
   , the random value is generated between 20 and 30 degrees with a random increment between -0.5 to 0.5 degrees.
- `HumiditySensor`: A sensor that measures humidity extending `Sensor` class and mapping a default initial value of 50.0, unit of percentage, a timestamp of the last sample in milliseconds.
   , the random value is generated between 40% and 60% percentage with a random increment between -5% to 5%.
- `SmartLight`: An actuator that can be turned on or off extending `Actuator` class and mapping a default initial status of `OFF`, a timestamp of the last action in milliseconds. The `invoke_action(action_type, payload)`
   method check the received action type and if it supported (`SWITCH` value) together with the correct value of the payload (`ON` or `OFF`) change the current value of the actuator and align the associated timestamp.

### Temperature Sensor Class

The Temperature Sensor class extends the `Sensor` class and implements both the init logic and the `update_measurement` method to generate random temperature values between 20 and 30 degrees with a random increment between -0.5 to 0.5 degrees.
The init method sets the initial temperature to 20 degrees, the unit to Celsius and the timestamp to the setup instance in milliseconds.

```python
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
```

The `update_measurement` method generates a random temperature value between 20 and 30 degrees with a random increment between -0.5 to 0.5 degrees.

```python
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
```

### Humidity Sensor Class

The Humidity Sensor class extends the `Sensor` class and implements both the init logic and the `update_measurement` method to generate random humidity values between 40% and 60% with a random increment between -5% to 5%.
The init method sets the initial humidity to 50%, the unit to percentage and the timestamp to the setup instance in milliseconds.

```python
import time
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
```
The `update_measurement` method generates a random humidity value between 40% and 60% with a random increment between -5% to 5%.

```python
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
```

### Smart Light Actuator Class

The Smart Light class extends the `Actuator` class and implements both the init logic and the `invoke_action` method to switch the light on or off.
The init method sets the initial status to `OFF` and the timestamp to the setup instance in milliseconds.

```python
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
```

The `invoke_action` method checks the received action type and if it supported (`SWITCH` value) together with the correct value of the payload (`ON` or `OFF`) change the current value of the actuator and align the associated timestamp.
The method checks if the action type is `SWITCH` and the payload is `ON` or `OFF` and then updates the status of the actuator.

```python
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
```

## Storage Management

The class `StorageManager` has been defined to shape how data are stored in the application, to centralize the associated methods and 
_hide_ how data and information are effectively stored by the class itself.

The actual implementation has the following main capabilities:

- **Device Description Storage**: allows to store and retrieve Devices for the Smart Home through dedicated method. The adopted data structure is a `list` of devices.
- **Device Json Measurement Storage**: supports the saving and retrieval of sensor measurements and actuator variations over time.

Implemented and supported methods are:

- `store_device_description(self, device_id, device_description)`: store a device description in the storage
- `remove_device_description(self, device_id)`: remove a device description from the storage
- `get_device_description(self, device_id)`: get a device description from the storage
- `get_all_device_descriptions(self)`: get all device descriptions from the storage
- `store_measurement(self, device_id, measurement)`: store a measurement in the storage
- `get_measurements(self, device_id)`: get all measurements for a device from the storage
- `get_all_measurements(self)`: get all measurements from the storage

The constructor initializes two dictionaries to store the device descriptions and the device measurements.

```python
class StorageManager:
    """ Class to manage the data storage of the smart home """

    def __init__(self):
        """ Initialize the data manager with an empty dictionary to store sensor data """
        self.device_description_dict = {}
        self.device_measurement_dict = {}
```

The methods to handle the device descriptions are the following:

```python
def store_device_description(self, device_id, device_description):
    """ Store a new device description """
    self.device_description_dict[device_id] = device_description

def remove_device_description(self, device_id):
    """ Remove a stored device description """
    if device_id in self.device_description_dict.keys():
        del self.device_measurement_dict[device_id]

def get_device_description(self, device_id):
    """ Get a device description by its ID """
    if device_id in self.device_description_dict.keys():
            return self.device_description_dict[device_id]
    else:
        return None

def get_all_device_descriptions(self):
    """ Return all the device Descriptions """
    return self.device_description_dict
```

On the other hand, the methods to handle the device measurements are the following:

```python
def store_measurement(self, device_id, measurement):
    """ Store a measurement for a devices. It can be associated both a variation of a Sensor or a status change in an actuator """
    if device_id not in self.device_measurement_dict:
        self.device_measurement_dict[device_id] = []
    self.device_measurement_dict[device_id].append(measurement)

def get_measurements(self, device_id):
    """ Get all measurements for a specific devices """
    return self.device_measurement_dict.get(device_id, [])

# Get all measurements for all devices
def get_all_measurements(self):
    """ Get all measurements for all devices """
    return self.device_measurement_dict
```

## Smart Home

The Smart Home class is in charge of the following responsibilities: 

- **Device Management**: Exposes the capabilities to manage devices (`add`, `remove`, and `get`) hiding the fact that it is also using an instance of the `StorageManager` to do that.
- - **Home Monitoring**: Implements a method to emulate the `monitoring` of the Smart Home that periodically check and update sensors measurements and randomly change actuators status and then store variation on through the `StorageManager`.
- **Measurement Service**: Exposes stored measurements associated to both sensors and actuators hiding the fact that it is using an instance of the `StorageManager` to do that.


The `SmartHome` constructor receives the `StorageManager` instance and the `home_id` and the `latitude` and `longitude` of the Smart Home.
Then initializes a dictionary to store active devices that have been added and managed by to the Smart Home.

```python
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
```

Then device management methods are implemented to add, remove, and get devices from the Smart Home.

```python
def add_device(self, device):
  """ Add a new devices to the smart home """

  # If the Class type is correct
  if isinstance(device, Device):
    # Add the Device to the internal structure
    self.device_dict[device.device_id] = device

    # Save the Device Description through the Data Manager
    self.storage_manager.store_device_description(device.device_id, device.get_json_description())
  else:
    raise TypeError("Expected Device Class ! Error a different type has been provided !")


def remove_device(self, device_id):
  """ Remove a devices from the smart home """

  if device_id in self.device_dict.keys():
    ## Remove the device from the internal structure and from the storage
    del self.device_dict[device_id]
    self.storage_manager.remove_device_description(device_id)
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
  return self.storage_manager.get_all_device_descriptions()
```

The SmartHome has also a method to exposes the collected measurements of the devices managed by the Smart Home through 
the internal usage of the Storage Manager.

```python
def get_all_measurements(self):
  """ Get all measurements for all devices """
  return self.storage_manager.get_all_measurements()
```

The core method of the Smart Home is the `monitor_home` that emulates the monitoring of the Smart Home that periodically check and update sensors measurements and randomly change actuators status and then store variation on through the `StorageManager`.

```python
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
        self.storage_manager.store_measurement(device.device_id, device.get_json_description())

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
          self.storage_manager.store_measurement(device.device_id, device.get_json_description())
```

## Main Application

The `main.py` file is the entry point of the application. It creates a Smart Home instance and adds some devices to it.
It also starts the monitoring of the Smart Home and prints the measurements of the devices.

```python
    # Create the smart home
my_smart_home = SmartHome(StorageManager(), "SH001", 37.7749, -122.4194)

# Add devices
temp_sensor = TemperatureSensor(device_id=1)
humidity_sensor = HumiditySensor(device_id=2)
smart_light = SmartLight(device_id=3)

my_smart_home.store_device_description(temp_sensor)
my_smart_home.store_device_description(humidity_sensor)
my_smart_home.store_device_description(smart_light)

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

## Managing Types in Python

Python is a dynamically typed language, but it supports type hints which can be used to indicate the types of variables, function parameters, and return values. 
These hints are not enforced at runtime but can help with code readability and tooling support.

Making a comparison with another programming language like Java, Python is a dynamically typed language, which means that the type of a variable is determined at runtime.
On the other hand, Java is a statically typed language, which means that the type of a variable is determined at compile time.

Main differences can be (briefly) summirized as follows:

**Python**:
- Dynamic Typing: Variables do not need to be declared with a type, and their type can change at runtime.
- Type Hints: Optional type hints can be used for better code clarity and tooling support but are not enforced at runtime.

**Java**:
- Static Typing: All variables must be declared with a type, and their type cannot change at runtime.
- Type Enforcement: The type of variable is enforced by the compiler at compile-time.

**In summary, Python's dynamic typing provides more flexibility, whereas Java's static typing offers more type safety and early error detection. 
Type hints in Python can bridge some of the gap by providing optional type information without losing the flexibility of dynamic typing.**

### Type Hints for Functions

Type hints can be used to specify the expected types of function parameters and return values.

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

In this example, the `name` parameter is expected to be a string, and the return value is also expected to be a string.

Example with Multiple Parameters and Return Types:

```python
def add(a: int, b: int) -> int:
    return a + b

def concatenate(strings: list[str]) -> str:
    return ' '.join(strings)
```

Here, `add` expects two integers and returns an integer, while `concatenate` expects a list of strings and returns a single concatenated string.

### Type Hints for Classes

Type hints can also be used in classes to indicate the types of attributes and the types of method parameters and return values.

```python
from typing import List

class Person:
    def __init__(self, name: str, age: int):
        self.name: str = name
        self.age: int = age
    
    def greet(self) -> str:
        return f"Hello, my name is {self.name} and I am {self.age} years old."
    
    def add_friends(self, friends: List[str]) -> None:
        self.friends: List[str] = friends
 ```

In the Person class, the `__init__` method initializes `name` and `age` attributes with type hints.
The `greet` method returns a string, and the `add_friends` method takes a list of strings as a parameter and returns nothing (None).

### Declaring Variable Types

You can also specify the types of variables outside of functions and classes.

```python
age: int = 25
name: str = "Alice"
is_student: bool = True
scores: list[int] = [85, 90, 78]
```

In these examples, `age` is an integer, `name` is a string, `is_student` is a boolean, and scores is a list of integers.

### Using Type Aliases

For complex types, you can create type aliases to simplify your code.
Probably in some cases is better to use a class instead of a type alias in order to have a more structured code with
parameters and behaviours for involved entities.

```python
from typing import Dict, Tuple

Coordinates = Tuple[float, float]
UserInfo = Dict[str, str]

location: Coordinates = (40.7128, -74.0060)
user: UserInfo = {"name": "Alice", "email": "alice@example.com"}
```

Here, Coordinates is a type alias for a tuple of two floats, and UserInfo is a type alias for a dictionary with string keys and string values.

### Possible Variable Types in Python

Here are some examples of possible variable types in Python:

- `int`: Integer
- `float`: Floating-point number
- `str`: String
- `bool`: Boolean
- `list`: List of elements
- `tuple`: Immutable sequence
- `dict`: Dictionary (key-value pairs)
- `set`: Set of unique elements
- `None`: Special constant representing the absence of a value

**In this playground, type hints have been only mentioned in this README in order to present a more structured code
and give you and idea of how to use them in your Python projects. In future projects and examples they might be integrated
in the code to provide a more structured and clear code, so please refer to this section for a brief overview of how to use them.**