from utime import sleep
from machine import Pin, PWM

F_MIN = 500
F_MAX = 1000

f = F_MIN
delta_f = 1

p = PWM(Pin(5), f)
print(p)

while True:
    p.freq(f)

    sleep(10 / F_MIN)

    f += delta_f
    if f >= F_MAX or f <= F_MIN:
        delta_f = -delta_f