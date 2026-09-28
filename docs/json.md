# JSON Introduction

This document introduces JSON and Python's built-in `json` module using examples taken from the IoT world
(sensors, actuators, gateways and smart homes).
Go back to the main [README](../README.md) for the Smart Home playground.

- [What is JSON](#what-is-json)
- [Basic components of JSON](#basic-components-of-json)
- [Import Json Package](#import-json-package)
- [Load JSON data from a file](#load-json-data-from-a-file)
- [Dump data to a JSON file](#dump-data-to-a-json-file)
- [Json & Dictionary](#json--dictionary)
- [How JSON is used in this Playground](#how-json-is-used-in-this-playground)

## What is JSON

JSON (JavaScript Object Notation) is a lightweight data-interchange format that is easy for humans to read and write, and easy for machines to parse and generate.
It is a text format that is completely language-independent, making it ideal for data exchange between different systems.

This is why JSON is one of the most common formats in IoT: a temperature sensor, a gateway, a cloud platform and a mobile app
can be written in different languages and run on very different hardware, but they can all read and write the same JSON messages.

An example of a JSON data structure describing a single temperature measurement is:

```json
{
  "device_id": "temp-sensor-01",
  "value": 21.5,
  "unit": "C"
}
```

## Basic components of JSON

Objects:
- Enclosed in curly braces (`{}`).
- Contain key-value pairs separated by commas.
- Keys are strings (enclosed in double quotes).
- Values can be any valid JSON data type (including objects, arrays, strings, numbers, booleans, or null).

Arrays:
- Enclosed in square brackets (`[]`).
- Contain ordered lists of values separated by commas.
- Values can be any valid JSON data type.

Data types in JSON (with IoT examples):

- Strings: Enclosed in double quotes (`"device_id": "smart-light-03"`, `"status": "ON"`).
- Numbers: Can be integers or floating-point numbers (`"timestamp": 1727535600000`, `"value": 48.7`).
- Booleans: `true` or `false` (`"online": true`, `"battery_low": false`).
- Null: Represents the absence of a value (`"value": null` for a sensor that has not produced any measurement yet).

Characteristics of JSON:

- Human-readable: a developer can open a device message or a configuration file and immediately understand it.
- Machine-readable: devices, gateways and cloud services can easily parse and generate it.
- Lightweight: JSON messages are relatively small compared to XML, an important aspect for constrained devices and networks.
- Language-independent: a sensor firmware in C, a gateway in Python and a dashboard in JavaScript can share the same data.
- Hierarchical: data is organized using nested objects and arrays (e.g., a home containing rooms containing devices).

Example of a richer JSON structure describing a device, combining all the data types, nested objects and arrays:

```json
{
  "device_id": "temp-sensor-01",
  "device_type": "TemperatureSensor",
  "device_manufacturer": "Acme Inc.",
  "online": true,
  "firmware_version": "1.4.2",
  "location": {
    "room": "kitchen",
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  "supported_units": ["C", "F", "K"],
  "last_measurement": {
    "value": 21.5,
    "unit": "C",
    "timestamp": 1727535600000
  },
  "error": null
}
```

## Import Json Package

Python provides built-in support for JSON through the `json` module (no installation required):

```python
import json
```

## Load JSON data from a file

A typical IoT use case is loading the configuration of the devices from a file. Given a `devices_config.json` file:

```json
{
  "home_id": "SH001",
  "devices": [
    {"device_id": "temp-sensor-01", "device_type": "TemperatureSensor", "sampling_period_ms": 1000},
    {"device_id": "hum-sensor-02", "device_type": "HumiditySensor", "sampling_period_ms": 5000},
    {"device_id": "smart-light-03", "device_type": "SmartLight"}
  ]
}
```

`json.load()` reads the file and converts it into Python objects (dictionaries and lists):

```python
with open('devices_config.json', 'r') as f:
    config = json.load(f)

print(config["home_id"])                     # Output: SH001
for device in config["devices"]:
    print(device["device_id"], device["device_type"])
```

## Dump data to a JSON file

Conversely, `json.dump()` writes Python objects to a file as JSON, for example to save the measurements collected by a sensor:

```python
measurements = [
    {"device_id": "temp-sensor-01", "value": 21.5, "unit": "C", "timestamp": 1727535600000},
    {"device_id": "temp-sensor-01", "value": 21.7, "unit": "C", "timestamp": 1727535601000},
    {"device_id": "temp-sensor-01", "value": 21.4, "unit": "C", "timestamp": 1727535602000}
]

with open('temperature_log.json', 'w') as f:
    json.dump(measurements, f, indent=2)
```

The optional `indent` parameter produces a nicely formatted (human-readable) file.

## Json & Dictionary

`json.dumps()` and `json.loads()` (with the final **s** for *string*) work with strings instead of files.
This is what happens when a device sends a message over the network: the data is converted into a JSON string before
being transmitted, and converted back into a dictionary by the receiver.

From Dictionary to Json String (e.g., a sensor preparing a message to send):

```python
measurement = {
    "device_id": "hum-sensor-02",
    "value": 48.7,
    "unit": "%RH",
    "timestamp": 1727535600000
}

json_message = json.dumps(measurement)
print(json_message)
```

The output will be:

```json
{"device_id": "hum-sensor-02", "value": 48.7, "unit": "%RH", "timestamp": 1727535600000}
```

From Json String to Dictionary (e.g., a smart light receiving a command):

```python
json_command = '{"device_id": "smart-light-03", "action_type": "SWITCH", "payload": "ON"}'
command = json.loads(json_command)

print(command["device_id"])     # Output: smart-light-03
print(command["action_type"])   # Output: SWITCH
print(command["payload"])       # Output: ON
```

## How JSON is used in this Playground

In the Smart Home playground JSON is the common format used to **describe devices** and to **report their measurements/status**.
Every device converts its own attributes into a Python dictionary and then serializes it into a JSON string with `json.dumps()`:

- `Device.get_json_description()` ([device.py](../src/smart_home/devices/device.py)) returns the description of a device (`device_id`, `device_type`, `device_manufacturer`).
  It is implemented once in the base class and inherited by every subclass.

  ```json
  {"device_id": 1, "device_type": "TemperatureSensor", "device_manufacturer": "Acme Inc."}
  ```

- `Sensor.get_json_measurement()` ([sensor.py](../src/smart_home/devices/sensor.py)) returns the last measurement of a sensor (`device_id`, `value`, `unit`, `timestamp`).

  ```json
  {"device_id": 1, "value": 20.3, "unit": "C", "timestamp": 1727535600000}
  ```

- `Actuator.get_json_measurement()` ([actuator.py](../src/smart_home/devices/actuator.py)) returns the last status of an actuator (`device_id`, `status`, `timestamp`).

  ```json
  {"device_id": 3, "status": "ON", "timestamp": 1727535600000}
  ```

These JSON strings are what the `StorageManager` ([storage_manager.py](../src/smart_home/data/storage_manager.py)) stores,
and what the `SmartHome` exposes when returning device descriptions and measurements.
Using a standard, language-independent text format means that the same data could later be saved to a file (`json.dump`),
sent over the network, or read by an application written in a different language, without changing the device classes.
