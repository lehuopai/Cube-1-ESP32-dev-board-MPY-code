import lvgl as lv
import time
from machine import Pin,I2C
from ili9XXX import ili9341


#-----------------屏幕初始化——————————————————
WIDTH=240
HEIGHT=240

#创建显示屏对象

disp=ili9341(miso=19,mosi=23,clk=18,cs=14,dc=27,rst=33,power=32,backlight=-1,
             backlight_on=0,power_on=1, mhz=40, factor=4, hybrid=False,
             width=WIDTH,height=HEIGHT,invert=False,double_buffer=True,half_duplex=False,initialize=True)
disp.set_pos(0,0)


I2C_SDA_PIN = const(21)
I2C_SCL_PIN = const(22)
I2C_FREQ = const(400000)
i2c_bus = I2C(1,sda=Pin(I2C_SDA_PIN), scl=Pin(I2C_SCL_PIN), freq=I2C_FREQ)

touch = uFT6336U.FT6336U(i2c_bus)
touch.get_positions()

#-------------------------

cw = lv.colorwheel(lv.scr_act(), True)
cw.set_size(200, 200)
cw.center()