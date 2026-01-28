from .EmulatorCore import LittleEndian, register, Ram, GrabBits, Memory
def __get_CPU_TYPES():
  return {"I8086": []}
class I8086():
  cps = 0
  t_X8=[]
  t_8=[lambda: GrabBits(self.ax, 0, 7), lambda: GrabBits(self.cx, 0, 7), lambda: GrabBits(self.dx, 0, 7), lambda: GrabBits(self.bx, 0, 7), lambda: GrabBits(self.ax, 8, 15), lambda: GrabBits(self.cx, 8, 15), lambda: GrabBits(self.dx, 8, 15), lambda: GrabBits(self.bx, 8, 15)]
  t_X_8 = [lambda: self.ram.read(self.bx+self.si), lambda: self.ram.read(self.bx+self.di), lambda: self.ram.read(self.bp+self.si), lambda: self.ram.read(self.bp+self.di), lambda:  self.ram.read(self.si), lambda: self.ram.read(self.di), lambda: self.ram.read(self.imm), lambda: self.ram.read(self.bx), lambda: self.ram.read(self.bx+self.si+self.imm), lambda: self.ram.read(self.bx+self.di+self.imm), lambda: self.ram.read(self.bp+self.si+self.imm), lambda: self.ram.read(self.bp+self.di+self.imm), lambda:  self.ram.read(self.si+self.imm), lambda: self.ram.read(self.di+self.imm), lambda: self.ram.read(self.bp+self.imm), lambda: self.ram.read(self.bx+self.imm)]
  t_X9 = []
  t_9=[lambda: self.ax, lambda: self.cx, lambda: self.dx, lambda: self.bx, lambda: self.sp, lambda: self.bp, lambda: self.si, lambda: self.di]
  t_X_9 = [lambda: LittleEndian([self.ram.read(self.bx+self.si), self.ram.read(self.bx+self.si+1)], 2), lambda: LittleEndian([self.ram.read(self.bx+self.di), self.ram.read(self.bx+self.di+1)], 2), lambda: LittleEndian([self.ram.read(self.bp+self.si), self.ram.read(self.bp+self.si+1)], 2), lambda: LittleEndian([self.ram.read(self.bp+self.di), self.ram.read(self.bp+self.di+1)], 2), lambda:  LittleEndian([self.ram.read(self.si), self.ram.read(self.si+1)], 2), lambda: LittleEndian([self.ram.read(self.di), self.ram.read(self.di+1)], 2), lambda: LittleEndian([self.ram.read(self.imm), self.imm+1],2), lambda: LittleEndian([self.ram.read(self.bx), self.ram.read(self.bx+1)], 2)]
  @staticmethod
  def DefaultMemMap():
    return Memory([(0x0, Ram())], 2**20-1)
  def __init__(self, ram, start=0xFFF0, startseg=0xF000):
    self.start = start
    self.segstart = segstart
    self.reset()
    if isinstance(ram, Ram):
      self.ram = ram
    elif isinstance(ram, Memory):
      self.ram = ram
    else:
      self.ram = Ram(ram)
    self.paused = False
    self.step = False
    self.ram.setAddressLimit(2**20-1) # pyright: ignore
  def reset(self):
    self.ax = register(size=16)
    self.bx = register(size=16)
    self.cx = register(size=16)
    self.dx = register(size=16)
    
    self.si = register(size=16)
    self.di = register(size=16)
    self.bp = register(size=16)
    self.sp = register(size=16)
    
    self.ip = register(self.start, size=16)
    
    self.cs = register(self.startseg, size=16)
    self.es = register(size=16)
    self.ss = register(size=16)
    self.ds = register(size=16)
    
    self.flags = register(size=16)
  def ramregister(self, address, register):
    
  def decode(self):
    i = self.ram.read(self.PC)
    if i in self.i_X9:
      byte1=self.ram.read(self.PC+1)
      byte1_9 = GrabBits(byte1, 3, 5)
      byte1_X = GrabBits(byte1, 0, 2) + (GrabBits(byte1, 6, 7)<<3)
      a=GrabBits(byte1, 6, 7)
      imm=0
      if a==1:
        imm=self.ram.read(self.PC+2)
      if a==2 or byte1_X==6:
        imm = LittleEndian([self.ram.read(self.PC+2), self.ram.read(self.PC+3)], 2)
      return (i, self.t_9[byte1_9], self.t_9_X[byte1_X], imm, 2 if a == 3 else 2+a)
  # Execute the next instruction in memory
  def execute(self):
    try:
      if self.paused:
        return
      self.instruct, self.reg_addr1, self.reg_addr2, self.imm, ilen= self.decode() 
      match self.instruct:

      self.ip+=ilen
    except Exception as e:
      print(e)
      for i in range(32):
        print(f'{["ax", "bx", "cx", "dx", "si", "di", "bp", "sp", "ip", "cs", "es", "ss", "ds", "flags"][i]}:{hex([self.ax, self.bx, self.cx, self,dx, self.si, self.di, self.bp, self.sp, self.ip, self.cs, self.es, self.ss, self.ds, self.flags][i].value)}', end=(", " if (i+1)%7!=0 else "\n"))
      self.paused = True
    finally:
      if self.step:
        self.paused = True
      self.cps += 1

