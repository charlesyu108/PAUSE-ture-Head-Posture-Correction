#Modified from: https://learn.adafruit.com/adafruit-vl6180x-time-of-flight-micro-lidar-distance-sensor-breakout/python-circuitpython?fbclid=IwAR0xaH46MN52O-F4GGNhsyI8-7WIeig0wsy4pUdKLb2weZFTG3MGKgPAv-I

import time, board, busio, adafruit_vl6180x, adafruit_tca9548a

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Init TCA multiplexer
tca = adafruit_tca9548a.TCA9548A(i2c)

# Init sensors from tca channels
sensor_left = adafruit_vl6180x.VL6180X(tca[2])
sensor_right = adafruit_vl6180x.VL6180X(tca[0])

def readSensors():
    left_mm = sensor_left.range
    right_mm = sensor_right.range
    print("Sensor Read", left_mm, right_mm)
    return (left_mm, right_mm)

