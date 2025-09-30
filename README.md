# Gyropen

A real-time IMU (Inertial Measurement Unit) data visualization system using ESP32 and MPU6050 sensor with web-based drawing interface.

## Overview

Gyropen is a system that reads accelerometer and gyroscope data from an MPU6050 sensor connected to an ESP32 microcontroller, processes the data using a complementary filter, and visualizes it in real-time through a web interface. The accelerometer data is used to create a live drawing on an HTML5 canvas, where the device orientation controls a drawing cursor.

## Features

- **Real-time IMU Data Processing**: Reads accelerometer and gyroscope data from MPU6050
- **Sensor Calibration**: Automatic calibration during startup for accurate readings
- **Complementary Filter**: Combines accelerometer and gyroscope data for stable angle estimation
- **Web-based Visualization**: Live drawing interface using HTML5 canvas
- **WebSocket Communication**: Real-time data streaming between ESP32 and web interface
- **Data Smoothing**: Low-pass filtering for smoother drawing experience

## System Architecture

``` ESP32 + MPU6050 → WiFi → FastAPI Server → WebSocket → Web Interface ```

### Components

1. **ESP32 Microcontroller** (`esp/server.py`)
   - Reads IMU data from MPU6050 sensor
   - Processes data with complementary filter
   - Sends data to server via HTTP POST

2. **FastAPI Server** (`server/main.py`)
   - Receives IMU data via REST API
   - Broadcasts data to web clients via WebSocket
   - CORS enabled for cross-origin requests

3. **Web Interface** (`server/index.html`)
   - Real-time visualization using HTML5 canvas
   - WebSocket client for live data streaming
   - Smooth drawing based on accelerometer input

## Hardware Requirements

- ESP32 development board
- MPU6050 IMU sensor
- Breadboard and jumper wires

### Wiring

| MPU6050 Pin | ESP32 Pin |
|-------------|-----------|
| VCC         | 3.3V      |
| GND         | GND       |
| SCL         | GPIO 22   |
| SDA         | GPIO 21   |

## Software Requirements

### Server Dependencies

Install the required Python packages:

```bash
pip install -r server/requirements.txt
```

Key dependencies:

- FastAPI
- Uvicorn
- WebSockets
- NumPy
- PyTorch (for potential ML features)

### ESP32 Setup

1. Install MicroPython on your ESP32
2. Upload `esp/server.py` to your ESP32
3. Update WiFi credentials and server IP in the code

## Configuration

### WiFi Settings (ESP32)

Update the WiFi credentials in `esp/server.py`:

```python
SSID = "your_wifi_name"
PASSWORD = "your_wifi_password"
```

### Server IP Configuration

Update the server IP address in both:

1. `esp/server.py`:

```python
SERVER_URL = "http://YOUR_SERVER_IP:8000/imu-data/"
```

2. `server/index.html`:

```javascript
const ws = new WebSocket("ws://YOUR_SERVER_IP:8000/ws");
```

## Installation & Usage

### 1. Setup the Server

```bash
# Navigate to server directory
cd server

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
python main.py
```

The server will start on `http://0.0.0.0:8000`

### 2. Configure and Deploy ESP32 Code

1. Update WiFi credentials and server IP in `esp/server.py`
2. Upload the code to your ESP32 using your preferred method (Thonny, ampy, etc.)
3. Reset the ESP32 to start the program

### 3. Open Web Interface

1. Open `server/index.html` in a web browser
2. Ensure the WebSocket URL matches your server IP
3. Move the ESP32 device to see real-time drawing on the canvas

## Calibration Process

The system automatically calibrates when the ESP32 starts:

1. Keep the device **still and upright** (LED facing up) during calibration
2. Calibration takes about 2 seconds (200 samples)
3. The system will print "Calibration done!" when complete

## Data Processing

### Sensor Data

- **Accelerometer**: Measures linear acceleration in g-force
- **Gyroscope**: Measures angular velocity in degrees/second
- **Sampling Rate**: 20 Hz (50ms intervals)

### Filtering

- **Complementary Filter**: Combines gyroscope and accelerometer data
- **Alpha Value**: 0.98 (98% gyroscope, 2% accelerometer for angle estimation)
- **Low-pass Filter**: Applied in web interface for smooth drawing

## API Endpoints

### POST `/imu-data/`

Receives IMU data from ESP32

**Request Body:**

```json
{
  "accel": [ax, ay, az],
  "gyro": [gx, gy, gz],
  "angle": [angle_x, angle_y]
}
```

### WebSocket `/ws`

Real-time data streaming to web clients

## Troubleshooting

### Common Issues

1. **WiFi Connection Failed**
   - Check SSID and password
   - Ensure ESP32 is within range
   - Verify network allows IoT devices

2. **No Data in Web Interface**
   - Verify server IP addresses match
   - Check if server is running on port 8000
   - Ensure firewall allows connections

3. **Erratic Drawing**
   - Recalibrate by restarting ESP32
   - Adjust smoothing parameters in web interface
   - Check sensor wiring connections

### Debug Output

The ESP32 provides serial output for debugging:

- WiFi connection status
- Calibration progress
- Sensor offset values
- HTTP request errors

## Customization

### Adjusting Sensitivity

In `server/index.html`, modify:

```javascript
const scale = 2; // Increase for more sensitive movement
const alpha = 0.2; // Adjust smoothing (0.1 = more smooth, 0.5 = more responsive)
```

### Filter Parameters

In `esp/server.py`, adjust:

```python
ALPHA = 0.98  # Complementary filter coefficient
dt = 0.05     # Sampling interval (20 Hz)
```

## License

This project is open source. Feel free to modify and distribute as needed.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
