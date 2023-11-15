from machine import Pin
import neopixel,time

pin = Pin(5,Pin.OUT)
np = neopixel.NeoPixel(pin,n=1,bpp=3,timing=1)


def main():

    
    while True:
        
        np.fill((255,255,255))
        np.write()
        time.sleep(0.5)
        np.fill((0,0,0))
        np.write()
        time.sleep(0.5)
        
if __name__ == "__main__":
    main()