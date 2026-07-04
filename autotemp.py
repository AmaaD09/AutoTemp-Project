import time
import board
import adafruit_dht
import asyncio
from kasa import SmartPlug

# ==========================================
# CONFIGURATION
# Users: Adjust these variables for your setup
# ==========================================

# 1. GPIO Pins for the two DHT11 Sensors
# Replace board.D4 and board.D5 with your actual GPIO pins
SENSOR_1_PIN = board.D4
SENSOR_2_PIN = board.D5

# 2. Temperature Thresholds (in Celsius)
# Fan turns ON if average temp goes above this
TEMP_THRESHOLD_ON = 30.0  
# Fan turns OFF if average temp drops below this
TEMP_THRESHOLD_OFF = 25.0 

# 3. Kasa Smart Plug IP Address
# Set the local IP address of your Kasa Smart Plug
SMART_PLUG_IP = "192.168.1.100"

# 4. Extended Run Time (in seconds)
# Minimum time the fan should stay on once triggered (e.g., 300 = 5 minutes)
MIN_RUN_TIME_SECONDS = 300

# Polling Interval (in seconds)
# How often to check the temperature
POLL_INTERVAL = 10

# ==========================================
# INITIALIZATION
# ==========================================

try:
    dht1 = adafruit_dht.DHT11(SENSOR_1_PIN)
except Exception as e:
    print(f"Error initializing DHT11 Sensor 1: {e}")

try:
    dht2 = adafruit_dht.DHT11(SENSOR_2_PIN)
except Exception as e:
    print(f"Error initializing DHT11 Sensor 2: {e}")

plug = SmartPlug(SMART_PLUG_IP)


def read_sensor(sensor, name):
    """
    Safely read from a DHT11 sensor. Returns temperature in C, or None if it fails.
    """
    try:
        temp = sensor.temperature
        return temp
    except RuntimeError as error:
        # Errors happen fairly often with DHT sensors, just keep going
        print(f"[{name}] Read error: {error.args[0]}")
        return None
    except Exception as error:
        sensor.exit()
        raise error

async def control_loop():
    """
    Main asynchronous control loop.
    """
    fan_is_on = False
    fan_turned_on_at = 0

    while True:
        temp1 = read_sensor(dht1, "Sensor 1")
        time.sleep(1) # Small delay between sensor reads
        temp2 = read_sensor(dht2, "Sensor 2")

        valid_temps = [t for t in (temp1, temp2) if t is not None]

        if valid_temps:
            avg_temp = sum(valid_temps) / len(valid_temps)
            print(f"Average Temp: {avg_temp:.1f} C (Valid readings: {len(valid_temps)}/2)")

            try:
                await plug.update()

                if avg_temp >= TEMP_THRESHOLD_ON and not fan_is_on:
                    print(f"Temperature {avg_temp:.1f} C exceeds threshold {TEMP_THRESHOLD_ON} C. Turning fan ON.")
                    await plug.turn_on()
                    fan_is_on = True
                    fan_turned_on_at = time.time()

                elif avg_temp <= TEMP_THRESHOLD_OFF and fan_is_on:
                    time_since_turned_on = time.time() - fan_turned_on_at
                    
                    if time_since_turned_on >= MIN_RUN_TIME_SECONDS:
                        print(f"Temperature {avg_temp:.1f} C is below {TEMP_THRESHOLD_OFF} C and minimum run time met. Turning fan OFF.")
                        await plug.turn_off()
                        fan_is_on = False
                    else:
                        remaining_time = MIN_RUN_TIME_SECONDS - time_since_turned_on
                        print(f"Temperature is low, but minimum run time not met. Fan staying on for {remaining_time:.0f} more seconds.")
            
            except Exception as e:
                print(f"Error communicating with smart plug: {e}")
        else:
            print("Failed to read from both sensors this cycle.")

        # Wait before the next poll
        await asyncio.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    print("Starting AutoTemp-Project Monitoring...")
    try:
        asyncio.run(control_loop())
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
    finally:
        dht1.exit()
        dht2.exit()
