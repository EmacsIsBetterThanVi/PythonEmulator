from EmulatorCore import register, Ram
class riscv32():
  def __init__(self, ram):
    self.registers = [register(0, lock=True)]
    for i in range(31):
        self.registers.append(register())
    self.pc = register()
    self.ram = ram
  # Execute the next instruction in memory, then increment the program counter by 4
  def tick(self):
    byte1 = self.ram.read(self.pc.get())
    byte2 = self.ram.read(self.pc.get()+1)
    byte3 = self.ram.read(self.pc.get()+2)
    byte4 = self.ram.read(self.pc.get()+3)
    self.pc += 4