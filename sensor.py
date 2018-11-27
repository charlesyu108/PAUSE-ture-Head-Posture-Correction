#Modified from: https://learn.adafruit.com/adafruit-vl6180x-time-of-flight-micro-lidar-distance-sensor-breakout/python-circuitpython?fbclid=IwAR0xaH46MN52O-F4GGNhsyI8-7WIeig0wsy4pUdKLb2weZFTG3MGKgPAv-I

import time, board, busio, adafruit_vl6180x, adafruit_tca9548a

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Init TCA multiplexer
tca = adafruit_tca9548a.TCA9548A(i2c)

# Init sensors from tca channels
sensor_left = adafruit_vl6180x.VL6180X(tca[2])
sensor_right = adafruit_vl6180x.VL6180X(tca[6])

def readSensors():
    left_mm = sensor_left.range
    right_mm = sensor_right.range
    return (left_mm, right_mm)


# # Main loop prints the range and lux every second:
# while True:
#     # Read the range in millimeters and print it.
#     range_mm = sensor.range
#     print('Range: {0}mm'.format(range_mm))
#     # Read the light, note this requires specifying a gain value:
#     # - adafruit_vl6180x.ALS_GAIN_1 = 1x
#     # - adafruit_vl6180x.ALS_GAIN_1_25 = 1.25x
#     # - adafruit_vl6180x.ALS_GAIN_1_67 = 1.67x
#     # - adafruit_vl6180x.ALS_GAIN_2_5 = 2.5x
#     # - adafruit_vl6180x.ALS_GAIN_5 = 5x
#     # - adafruit_vl6180x.ALS_GAIN_10 = 10x
#     # - adafruit_vl6180x.ALS_GAIN_20 = 20x
#     # - adafruit_vl6180x.ALS_GAIN_40 = 40x
#     light_lux = sensor.read_lux(adafruit_vl6180x.ALS_GAIN_1)
#     print('Light (1x gain): {0}lux'.format(light_lux))
#     # Delay for a second.
#     time.sleep(1.0)
