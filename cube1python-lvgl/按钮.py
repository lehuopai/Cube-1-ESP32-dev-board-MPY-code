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
scr = lv.obj()


# 2. 封装的需要显示的按钮
class CounterBtn():
    def __init__(self, scr):
        self.cnt = 0
        btn = lv.btn(scr)  # 将当前按钮与screen对象进行关联
        # btn.set_pos(20, 10)  # 相对于屏幕左上角 x为20，y为10
        btn.set_size(120, 50)  # 设置按钮的宽度为120, 高度为50
        btn.align(lv.ALIGN.CENTER,0,0)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        btn.add_event_cb(self.btn_event_cb, lv.EVENT.ALL, None)  # 设置按钮被按下后的回调函数
        label = lv.label(btn)  # 在按钮上创建一个标签Label，用来显示文字用
        label.set_text("Button")  # 设置文字内容
        label.center()  # 相对于父对象居中

    def btn_event_cb(self, evt):
        code = evt.get_code()  # 获取点击事件类型码
        btn = evt.get_target()  # 获取被点击的对象，此时就是按钮
        if code == lv.EVENT.CLICKED:
            self.cnt += 1

        # Get the first child of the button which is the label and change its text
        label = btn.get_child(0)
        label.set_text("Button: " + str(self.cnt))  # 修改文字内容


# 3. 创建按钮
counterBtn = CounterBtn(scr)

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

