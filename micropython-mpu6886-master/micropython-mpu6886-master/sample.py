import utime
from machine import SoftI2C, Pin
from mpu6886 import MPU6886

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
sensor = MPU6886(i2c)

print("MPU6886 id: " + hex(sensor.whoami))

while True:
    print(sensor.acceleration)
    print(sensor.gyro)
    print(sensor.temperature)

    utime.sleep_ms(1000)