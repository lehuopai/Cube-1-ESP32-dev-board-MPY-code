import neopixel
import machine

pin = machine.Pin(5, machine.Pin.OUT)

n = neopixel.NeoPixel(pin, 1)

n[0] = (127, 0, 0)

n.write()

#https://vimsky.com/examples/detail/python-method-neopixel.NeoPixel.html