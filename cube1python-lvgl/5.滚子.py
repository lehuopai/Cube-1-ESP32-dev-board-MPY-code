import lvgl as lv       
import sys
from machine import I2C,Pin,SPI
from ili9XXX import ili9341
from ft6x36 import ft6x36
import utime as time


#-----------------屏幕初始化---------------------------
WIDTH=320
HEIGHT=240

#创建显示屏对象
disp=ili9341(miso=19,mosi=23,clk=18,cs=14,dc=27,rst=33,power=32,backlight_on=0,power_on=1, mhz=40, factor=4, rot=0,hybrid=False,width=WIDTH,height=HEIGHT,start_x=0,start_y=0,invert=True,double_buffer=True,half_duplex=False,initialize=True)
i2c_bus = I2C(1,sda=Pin(21), scl=Pin(22))

#创建触控对象
touch=ft6x36()

#------------------------------------------------------



#-------------------------------------------------------
lv.init()
scr = lv.scr_act()

def event_handler(e):
    code = e.get_code()
    obj = e.get_target()
    if code == lv.EVENT.VALUE_CHANGED:
        option = " "*10
        obj.get_selected_str(option, len(option))
        print("Selected app: " + option.strip())

#
# An infinite roller with the name of the months
#

roller1 = lv.roller(lv.scr_act())
roller1.set_options("\n".join([
    "mpu6050",
    "mp3",
    "drone",
    "game",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"]),lv.roller.MODE.INFINITE)

roller1.set_visible_row_count(4)
roller1.center()
roller1.add_event_cb(event_handler, lv.EVENT.ALL, None)

lv.scr_load(scr)


