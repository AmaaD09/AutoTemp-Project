# AutoTemp How-To Guide 

This guide walks you through hardware connections, software installation, local configuration, testing, and production deployment of the **AutoTemp** climate control system.

---

## 1. Hardware Connections & Setup

AutoTemp uses two DHT11 sensors to measure temperature at different heights or locations in an area, averaging them to avoid false readings.

### Sensor Pinout Reference
A standard DHT11 sensor typically has 3 or 4 pins:
- **VCC (Power)**: Connect to **3.3V** on the Raspberry Pi.
- **GND (Ground)**: Connect to **GND** on the Raspberry Pi.
- **DATA (Signal)**: Connect to a GPIO Pin on the Raspberry Pi.

> [!NOTE]
> If you are using a bare 4-pin DHT11 chip (instead of a 3-pin breakout board), you must place a **10k ohm pull-up resistor** between the VCC and DATA pins to stabilize the signal. If you use a 3-pin breakout module, the pull-up resistor is usually built in.

### Pinout Mapping
The default configuration in [`autotemp.py`](file:///c:/Users/Genra/Documents/amaad%20work/AutoTemp-Project/autotemp.py) is:
- **Sensor 1 (DATA)** ➡️ **GPIO 4 (board.D4)**
- **Sensor 2 (DATA)** ➡️ **GPIO 5 (board.D5)**

---

## 2. Software Installation

AutoTemp requires Python 3.7+ and several host system dependencies.

### Step 1: Install System Dependencies
On newer versions of Raspberry Pi OS (Bookworm and later), the Adafruit DHT library relies on `gpiod` for GPIO access. Install it using apt:
```bash
sudo apt update
sudo apt install -y python3-dev python3-pip libgpiod-dev gpiod
```

### Step 2: Set Up a Virtual Environment (Recommended)
Raspberry Pi OS prevents installing pip packages globally. Set up a dedicated Python virtual environment:
```bash
# Navigate to project directory
cd "/Users/Genra/Documents/work/AutoTemp-Project"

# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### Step 3: Install Python Dependencies
With the virtual environment activated, install the libraries listed in [`requirements.txt`](file:///c:/Users/Genra/Documents/amaad%20work/AutoTemp-Project/requirements.txt):
```bash
pip install -r requirements.txt
```

---

## 3. Finding the Kasa Smart Plug IP Address

To control your fan or heater, AutoTemp needs the local IP address of your Kasa smart plug.
1. Connect your Kasa smart plug to the same local Wi-Fi network as the Raspberry Pi using the Kasa mobile app.
2. In the app, tap the plug and go to Device Info/Settings to find its IP address (e.g. `192.168.1.100`).
3. Alternatively, with your virtual environment active, use the command-line utility to auto-discover local kasa devices:
   ```bash
   kasa discover
   ```
4. Note down the IP address.

---

## 4. Configuration

Open [`autotemp.py`](file:///c:/Users/Genra/Documents/amaad%20work/AutoTemp-Project/autotemp.py) in your editor and modify the configuration section at the top of the file:

```python
# ==========================================
# CONFIGURATION
# ==========================================

# 1. GPIO Pins for the two DHT11 Sensors
SENSOR_1_PIN = board.D4  # GPIO 4
SENSOR_2_PIN = board.D5  # GPIO 5

# 2. Temperature Thresholds (in Celsius)
TEMP_THRESHOLD_ON = 30.0  # Turn fan ON above this temp
TEMP_THRESHOLD_OFF = 25.0 # Turn fan OFF below this temp

# 3. Kasa Smart Plug IP Address
SMART_PLUG_IP = "192.168.1.100"  # Set to your smart plug's IP

# 4. Extended Run Time (in seconds)
MIN_RUN_TIME_SECONDS = 300  # Minimum fan run time (e.g., 5 mins)

# Polling Interval (in seconds)
POLL_INTERVAL = 10  # Check temperature every 10 seconds
```

---

## 5. Testing & Running

### Testing a Single Sensor
Before running the main controller, verify that the Raspberry Pi can read from a single sensor on GPIO 4 using the test script:
```bash
python temp2.py
```
If working, you will see output like:
`Temp: 24.0 C    Humidity: 55%`
Press `Ctrl+C` to stop.

### Running the Main Controller
Run the main script to start monitoring and automated control:
```bash
python autotemp.py
```
AutoTemp will display:
```text
Starting AutoTemp-Project Monitoring...
Average Temp: 28.5 C (Valid readings: 2/2)
Average Temp: 30.2 C (Valid readings: 2/2)
Temperature 30.2 C exceeds threshold 30.0 C. Turning fan ON.
```

---

## 6. Continuous Deployment (Running as a Service)

To run AutoTemp constantly in the background and ensure it launches automatically when the Raspberry Pi boots up, configure it as a `systemd` service:

1. Create a systemd service file:
   ```bash
   sudo nano /etc/systemd/system/autotemp.service
   ```

2. Paste the following configuration, replacing paths and user details as necessary:
   ```ini
   [Unit]
   Description=AutoTemp Climate Control Daemon
   After=network.target

   [Service]
   Type=simple
   User=pi
   WorkingDirectory=/home/pi/AutoTemp-Project
   ExecStart=/home/pi/AutoTemp-Project/venv/bin/python /home/pi/AutoTemp-Project/autotemp.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. Reload systemd, enable the service, and start it:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable autotemp.service
   sudo systemctl start autotemp.service
   ```

4. Check the service status:
   ```bash
   sudo systemctl status autotemp.service
   ```

5. Monitor the real-time logs:
   ```bash
   sudo journalctl -u autotemp.service -f
   ```
