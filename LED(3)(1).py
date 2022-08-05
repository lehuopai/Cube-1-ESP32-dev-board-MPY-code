import esp32
from esp32 import RMT
from machine import Pin
import time

#CONSTANTS
TEST_CL = [
  "#FF0000",
  "#FFFF00",
  "#FFFFFF",
  "#00FF00",
  "#00FFFF",
  "#0000FF",
  "#FF0000",
  "#FFFF00",
  "#FFFFFF",
  "#00FF00",
  "#00FFFF",
  "#0000FF",
  "#FF0000",
  "#FFFF00",
  "#FFFFFF",
  "#00FF00",
  "#00FFFF",
  "#0000FF",
]

class LED():
  LOW_P = [3,9]
  HIGH_P = [6,6]
  def __init__(self, io = Pin(5), num = 1):
    self.io = io
    self.num = num
    self.buf = (self.LOW_P * 24)*num
    self.rmt = esp32.RMT(0, pin=io, clock_div=8)
  def get_raw_via_hex(self, color):
    _buf = [] # 24
    if type (color) == str:
      color = color.lstrip('#')
      lv = len(color)
      color = tuple(int(color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    for c in (color[1], color[0], color[2]):
      x = bin(c)
      x = x[2: len(x)]
      if len(x) != 8:
        c = 8 - len(x)
        x = '0'*c + x
      for j in x:
        if j == '0':
          _buf.append(self.LOW_P[0])
          _buf.append(self.LOW_P[1])
        else:
          _buf.append(self.HIGH_P[0])
          _buf.append(self.LOW_P[1])
    return _buf
  def set(self, i, color):
    _buf = self.get_raw_via_hex(color)
    self.buf[(i-1)*24*2 : (i*24*2)-2] = _buf
  def rshift(self, add): #閸欏磭些
    self.buf = self.get_raw_via_hex(add) + self.buf
    l = len(self.buf)
    del self.buf[l-24: l]
  def clear(self):
    self.buf = (self.LOW_P * 24)*self.num
  def off(self):
    self.rmt.write_pulses(tuple((self.LOW_P*24)*self.num))
  def light(self):
    self.rmt.write_pulses(tuple((self.HIGH_P*24)*self.num))
  def render(self):
    # print(tuple(self.buf))
    self.rmt.write_pulses(tuple(self.buf))
  def get_raw(self, i):
    return self.buf[(i-1)*24*2 : (i*24*2)-2]
  def get(self, i):
    raw = self.get_raw(i)
    r = int(raw[0:7], 2)
    g = int(raw[7:15], 2)
    b = int(raw[15:23], 2)
    return (r, g, b)
  def set_all(self, color):
    color = self.get_raw_via_hex(color)
    self.buf = color * self.num
  def test_run_flash(self, colorlist, delay):
    for c in colorlist:
      self.set_all(c)
      self.render()
      time.sleep(delay/2)
      self.off()
      time.sleep(delay/2)
  def test_run_shift_colorful(self, colorlist, delay):
    for c in colorlist:
      self.rshift(c)
      self.render()
      time.sleep(delay)
      
#   led = LED (io=pin(21), num=80)
#   led.test_run_shift_colorful(TSET_CL ,0.5)
