import time
import board
import adafruit_dht

# Initialize the DHT11 device
# 'board.D4' corresponds to GPIO Pin 4
dhtDevice = adafruit_dht.DHT11(board.D4)

while True:
    try:
        # Print the values to the console
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        
        print(f"Temp: {temperature_c:.1f} C    Humidity: {humidity}%")

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)
