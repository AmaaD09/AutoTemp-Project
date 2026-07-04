# AutoTemp 🌡️🔌

AutoTemp is a lightweight, automated thermostat control system designed to run on low-power devices like the Raspberry Pi. By reading environmental data from dual DHT11 temperature/humidity sensors and averaging the measurements, AutoTemp intelligently switches a smart outlet (specifically a TP-Link Kasa Smart Plug) on or off to regulate climate controls (such as fans, heaters, or AC units) in a room or enclosure.

---

## Key Features

- **Dual Sensor Averaging**: Combines temperature data from two independent DHT11 sensors to filter out erroneous readings and local heat spikes.
- **TP-Link Kasa Integration**: Wirelessly manages kasa smart plugs (`python-kasa`) to trigger fans or climate-control hardware.
- **Asynchronous Poll Loop**: Powered by Python's `asyncio` for non-blocking sensor readings and plug updates.
- **Hysteresis Thresholds**: Uses separate temperature thresholds for turning on (`TEMP_THRESHOLD_ON`) and turning off (`TEMP_THRESHOLD_OFF`) to avoid constant power cycling.
- **Short-Cycling Protection**: Enforces a configurable minimum fan run-time (`MIN_RUN_TIME_SECONDS`) to preserve the lifespan of your cooling/heating devices.
- **Robust Error Handling**: Gracefully logs sensor timeouts and plug communication issues, continuing operation without crashing.

---

## Repository Structure

- [`autotemp.py`](file:///c:/Users/Genra/Documents/amaad%20work/AutoTemp-Project/autotemp.py): The main automation script containing configuration options, asynchronous logic, sensor averaging, and kasa control.
- [`temp2.py`](file:///c:/Users/Genra/Documents/amaad%20work/AutoTemp-Project/temp2.py): A helper script for testing a single DHT11 sensor setup on a specific GPIO pin (defaults to pin 4/D4).
- [`requirements.txt`](file:///c:/Users/Genra/Documents/amaad%20work/AutoTemp-Project/requirements.txt): List of python library dependencies required to run the scripts.

---

## Hardware Overview

To run AutoTemp, you typically need:
1. **Host Device**: Raspberry Pi (or a similar board with GPIO pins supporting Python/Adafruit DHT).
2. **Temperature Sensors**: 2x DHT11 sensors (with 10k ohm pull-up resistors, or DHT11 module boards with built-in resistors).
3. **Smart Outlet**: A TP-Link Kasa Smart Plug connected to the same local network.
4. **Appliance**: A fan, portable heater, or other plug-in climate control hardware.

---

## Getting Started

Ready to set up AutoTemp? Follow the step-by-step instructions in the [How-To Guide (HOWTO.md)](file:///c:/Users/Genra/Documents/amaad%20work/AutoTemp-Project/HOWTO.md) to wire the sensors, set up the software environment, configure your settings, and deploy AutoTemp as a system service.
