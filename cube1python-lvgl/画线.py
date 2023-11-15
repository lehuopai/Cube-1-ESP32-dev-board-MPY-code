import lvgl as lv       
import sys
from machine import I2C,Pin,SPI
from ili9XXX import ili9341
from ft6x36 import ft6x36
import utime as time
import fs_driver


#-----------------屏幕初始化---------------------------
WIDTH=320
HEIGHT=240

#创建显示屏对象
disp=ili9341(miso=19,mosi=23,clk=18,cs=14,dc=27,rst=33,power=32,backlight_on=0,power_on=1, mhz=40, factor=4, rot=0,hybrid=False,width=WIDTH,height=HEIGHT,start_x=0,start_y=0,invert=True,double_buffer=True,half_duplex=False,initialize=True)
i2c_bus = I2C(1,sda=Pin(21), scl=Pin(22))

#创建触控对象
touch=ft6x36()
# ------------------------------ 屏幕初始化操作 --stop------------------------

# 1. 创建显示screen对象。将需要显示的组件添加到这个screen才能显示
scr = lv.obj()  # scr====> screen 屏幕
fs_drv = lv.fs_drv_t()
fs_driver.fs_register(fs_drv, 'S')
scr = lv.scr_act()
scr.clean()


# 2. 封装要显示的组件
class MyWidget():
    def __init__(self, scr):
        # 创建 线 对象
        obj_line = lv.line(scr)
        
        # 创建样式
        style = lv.style_t()
        style.init()
        style.set_line_color(lv.palette_main(lv.PALETTE.GREY))
        style.set_line_width(6)
        style.set_line_rounded(True)
        
        # 添加样式
        obj_line.add_style(style, 0)
        
        point =  [{"x": 10, "y": 30}, {"x": 30, "y": 50}, {"x": 100, "y": 0}]

        obj_line.set_points(point, len(point))

        obj_line.center()


# 3. 创建要显示的组件
MyWidget(scr)

# 4. 显示screen对象中的内容
lv.scr_load(scr)



# ------------------------------ 看门狗，用来重启ESP32设备 --start------------------------
try:
    from machine import WDT
    wdt = WDT(timeout=1000)  # enable it with a timeout of 2s
    print("提示: 按下Ctrl+C结束程序")
    while True:
        wdt.feed()
        time.sleep(0.9)
except KeyboardInterrupt as ret:
    print("程序停止运行，ESP32已经重启...")
# ------------------------------ 看门狗，用来重启ESP32设备 --stop-------------------------

