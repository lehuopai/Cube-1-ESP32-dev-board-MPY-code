class TouchKey:  
  def __init__(self, i2c, irq, addr = 0x38):
    self.i2c = i2c
    self.addr = addr
    self.irq = irq
    self.i2c.writeto(self.addr, b'\0\0')
    self.i2c.writeto(self.addr, b'\xA4\x00')
  def write_reg(self, r, v):
    self.i2c.writeto(self.addr, r)
    self.i2c.writeto(self.addr, v)
  def read_reg(self, r):
    self.i2c.writeto(self.addr, r)
    return self.i2c.readfrom(self.addr, 1)[0]
  def read_(self, reg, buf, len):
    self.i2c.writeto(self.addr, reg)
    d = self.i2c.readfrom(self.addr, len)
    for i in range(0, len):
      buf[i] = d[i]
  def touchPos(self):
    buf = bytearray(40)
    self.read_(b'\3', buf, 6)
    x = (buf[0] & 0x0f) << 8 | buf[1]
    y = ((buf[2] & 0x0f) << 8 | buf[3])
    return (x,y)
  def touched(self):
    s = self.read_reg(b'\2')
    return not ((s & 0x0f) == 0)
  def touch_num(slf):
    s = self.read_reg(b'\2')
    return (s & 0x0f)
  