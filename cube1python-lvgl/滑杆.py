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
        # 创建滑块slider组件
        self.slider = lv.slider(scr)
        self.slider.set_width(200)  # 设置滑块的宽度
        #self.slider.set_range(10, 50)  # 默认值是0-100
        self.slider.center()  # 在窗口的中间位置
        self.slider.add_event_cb(self.slider_event_cb, lv.EVENT.VALUE_CHANGED, None)  # 添加回调函数

        # 创建一个标签label
        self.label = lv.label(scr)
        self.label.set_text("0")  # 默认值
        self.label.align_to(self.slider, lv.ALIGN.OUT_TOP_MID, 0, -15)  # label的中间与滑块的上外边框中间对齐，然后y向上15像素 x不变

    def slider_event_cb(self, evt):
        slider = evt.get_target()
        # 修改label的值
        self.label.set_text(str(slider.get_value()))



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

