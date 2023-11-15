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
        # Create an image from the png file
        try:
            with open('./settings.png', 'rb') as f:
                png_data = f.read()
        except:
            print("找不到图片文件...")
            sys.exit()

        img = lv.img_dsc_t({"data_size": len(png_data),"data": png_data})

        # 创建样式
        img_style = lv.style_t()
        img_style.init()
        # 设置背景颜色，圆角
        img_style.set_radius(5)
        img_style.set_bg_opa(lv.OPA.COVER)
        img_style.set_bg_color(lv.palette_lighten(lv.PALETTE.GREY, 3))
        # 设置边框以及颜色
        img_style.set_border_width(2)
        img_style.set_border_color(lv.palette_main(lv.PALETTE.BLUE))

        # 创建lvgl中的图片组件
        obj = lv.img(scr)
        # 添加图片数据
        obj.set_src(img)
        # 添加样式
        obj.add_style(img_style, 0)

        # 将图片居中
        obj.center()


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

