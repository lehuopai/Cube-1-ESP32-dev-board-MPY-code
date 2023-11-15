import lvgl as lv
import sys
from machine import I2C,Pin,SPI
from ili9XXX import ili9341
from ft6x36 import ft6x36
import utime as time
import fs_driver
import machine
import utime


# ----------------- 屏幕初始化 --start---------------------------
WIDTH=320
HEIGHT=240

# 创建显示屏对象
disp=ili9341(miso=19,mosi=23,clk=18,cs=14,dc=27,rst=33,power=32,backlight_on=0,power_on=1, mhz=40, factor=4, rot=0,hybrid=False,width=WIDTH,height=HEIGHT,start_x=0,start_y=0,invert=True,double_buffer=True,half_duplex=False,initialize=True)
i2c_bus = I2C(1,sda=Pin(21), scl=Pin(22))

# 创建触控对象
touch=ft6x36()
# ------------------------------ 屏幕初始化操作 --stop------------------------


# 1. 创建显示screen对象。将需要显示的组件添加到这个screen对象才能显示
scr = lv.obj()  # scr====> screen 屏幕
fs_drv = lv.fs_drv_t()
fs_driver.fs_register(fs_drv, 'S')
scr = lv.scr_act()
scr.clean()


# 2. 封装需要显示的标签
class InforLbl():
    def __init__(self, scr):
        self.cnt = 0
        lbl = lv.label(scr)  # 将当前标签与screen对象进行关联
        #lbl.set_pos(0, 10)  # 标签定位，相对于屏幕左上角，x为0，y为10
        #lbl.align(lv.ALIGN.CENTER, -20, 50)  # 标签对齐，居中偏移（x偏移-20，y偏移50）
        lbl.center()  # 相对于父对象居中
        lbl.set_size(320, 40)  # 设置标签的宽度为320, 高度为40
        self.myfont_cn = lv.font_load("S:./simfang-40.bin")  # 装载字体文件
        lbl.set_style_text_font(self.myfont_cn, 0)  # 设置标签字体
        lbl.set_text("RubikCube1欢迎你")  # 设置标签文字内容
        
# 3. 创建标签
inforLbl = InforLbl(scr)
 
# 4. 显示screen对象中的内容
lv.scr_load(scr)
 

# ------------------------------ 看门狗，用来重启ESP32设备 --start------------------------
try:
    from machine import WDT
    wdt = WDT(timeout = 1000)  # ESP32上，最小超时时间为1秒。1秒内未喂狗（程序跑飞），ESP复位
    print("提示：Ctrl+C结束")
    while True:    
        wdt.feed()
        time.sleep(0.9)
except KeyboardInterrupt as ret:
    print("程序停止运行，ESP32已经重启...")
# ------------------------------ 看门狗，用来重启ESP32设备 --stop-------------------------

