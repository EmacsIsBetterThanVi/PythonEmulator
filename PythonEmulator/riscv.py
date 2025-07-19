from EmulatorCore import register, Ram
class riscv32():
  rtype = []
  itype = []
  stype = []
  btype = []
  utype = []
  jtype = []
  def __init__(self, ram):
    self.registers = [register(0, lock=True)]
    for i in range(31):
        self.registers.append(register())
    self.pc = register()
    self.ram = ram
  # Execute the next instruction in memory, then increment the program counter by 4
  def decode(self):
    byte1 = self.ram.read(self.pc.get())
    byte2 = self.ram.read(self.pc.get()+1)
    byte3 = self.ram.read(self.pc.get()+2)
    byte4 = self.ram.read(self.pc.get()+3)
    self.pc += 4
    opcode = byte1 & 0b111111
    rd = 0
    rs1 = 0
    rs2 = 0
    funct3 = 0
    funct7 = 0
    imm = 0
    if opcode in rtype: