import sys
import time
import Adafruit_DHT

# Sensor type: 11 for DHT11, 22 for DHT22/AM2302
SENSOR_TYPE = 11
# GPIO Pin number (BCM mode)
GPIO_PIN = 4

print(f"Reading DHT{SENSOR_TYPE} on Pin {GPIO_PIN}...")

try:
    while True:
        # read_retry attempts to read up to 15 times (waiting 2s between retries)
        humidity, temperature = Adafruit_DHT.read_retry(SENSOR_TYPE, GPIO_PIN)

        # Check if reading was successful before printing
        if humidity is not None and temperature is not None:
            # Using f-string formatting (Python 3.6+)
            print(f'Temp: {temperature:0.1f} C  Humidity: {humidity:0.1f} %')
        else:
            print('Failed to get reading. Try again!')

        # Wait 2 seconds before the next read to ensure sensor stability
        time.sleep(2)

except KeyboardInterrupt:
    print("\nExiting gracefully...")
    sys.exit(0)
