import network
import urequests
import time
from machine import Pin, I2C

# ====== WIFI CONFIG ======
SSID = "arduino"
PASSWORD = "test@1234"

print("Connecting to WiFi...")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

timeout = 15  # seconds
start = time.time()
while not wlan.isconnected():
    if time.time() - start > timeout:
        print("WiFi connection failed!")
        break
    print("Waiting for connection...")
    time.sleep(1)

print("Connected! IP:", wlan.ifconfig()[0])

# ====== SERVER CONFIG ======
SERVER_URL = "http://10.165.146.205:8000/imu-data/"

# ====== MPU CONFIG ======
MPU_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
i2c.writeto_mem(MPU_ADDR, PWR_MGMT_1, b'\x00')  # wake up MPU

# ====== FUNCTIONS ======
def read_word(reg):
    data = i2c.readfrom_mem(MPU_ADDR, reg, 2)
    return int.from_bytes(data, "big", True)

def read_raw():
    ax = read_word(ACCEL_XOUT_H)
    ay = read_word(ACCEL_XOUT_H + 2)
    az = read_word(ACCEL_XOUT_H + 4)

    gx = read_word(GYRO_XOUT_H)
    gy = read_word(GYRO_XOUT_H + 2)
    gz = read_word(GYRO_XOUT_H + 4)

    return ax, ay, az, gx, gy, gz

# ====== CALIBRATION ======
print("Calibrating... Keep device still & upright (LED UP)")
N = 200
accel_offsets = [0, 0, 0]
gyro_offsets = [0, 0, 0]

for _ in range(N):
    ax, ay, az, gx, gy, gz = read_raw()
    accel_offsets[0] += ax
    accel_offsets[1] += ay - 16384
    accel_offsets[2] += az
    gyro_offsets[0] += gx
    gyro_offsets[1] += gy
    gyro_offsets[2] += gz
    time.sleep(0.01)

accel_offsets = [x / N for x in accel_offsets]
gyro_offsets = [x / N for x in gyro_offsets]

print("Calibration done!")
print("Accel offsets:", accel_offsets)
print("Gyro offsets:", gyro_offsets)

# ====== FILTERING ======
ALPHA = 0.98  # complementary filter coefficient
prev_angle_x = 0
prev_angle_y = 0
dt = 0.05  # 20 Hz

# ====== MAIN LOOP ======
def read_imu():
    global prev_angle_x, prev_angle_y
    ax, ay, az, gx, gy, gz = read_raw()

    # Apply offsets
    ax -= accel_offsets[0]
    ay -= accel_offsets[1]
    az -= accel_offsets[2]
    gx -= gyro_offsets[0]
    gy -= gyro_offsets[1]
    gz -= gyro_offsets[2]

    # Scale
    ax, ay, az = ax / 16384.0, ay / 16384.0, az / 16384.0
    gx, gy, gz = gx / 131.0, gy / 131.0, gz / 131.0

    # Compute accelerometer angles
    import math
    accel_angle_x = math.atan2(ay, math.sqrt(ax*ax + az*az)) * 180 / math.pi
    accel_angle_y = math.atan2(-ax, math.sqrt(ay*ay + az*az)) * 180 / math.pi

    # Complementary filter
    angle_x = ALPHA * (prev_angle_x + gx * dt) + (1 - ALPHA) * accel_angle_x
    angle_y = ALPHA * (prev_angle_y + gy * dt) + (1 - ALPHA) * accel_angle_y

    prev_angle_x = angle_x
    prev_angle_y = angle_y

    return {"accel": [ax, ay, az], "gyro": [gx, gy, gz], "angle": [angle_x, angle_y]}

while True:
    data = read_imu()
    try:
        res = urequests.post(SERVER_URL, json=data)
        res.close()
    except Exception as e:
        print("Error sending data:", e)
    time.sleep(dt)
