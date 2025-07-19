from .EmulatorCore import LittleEndian, register, Ram, GrabBits
class riscv32():
  rtype = [0b0110011]
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
    if isinstance(ram, Ram):
      self.ram = ram
    else:
      self.ram = Ram(ram)
  # Decode the next instruction in memory, then increment the program counter by 4
  def decode(self):
    byte1 = self.ram.read(self.pc.get())
    byte2 = self.ram.read(self.pc.get()+1)
    byte3 = self.ram.read(self.pc.get()+2)
    byte4 = self.ram.read(self.pc.get()+3)
    instruction = LittleEndian([byte1, byte2, byte3, byte4], 4)
    self.pc += 4
    opcode = GrabBits(instruction, 0, 6)
    rd = 0
    rs1 = 0
    rs2 = 0
    funct3 = 0
    funct7 = 0
    imm = 0
    if opcode in self.rtype:
      rd = GrabBits(instruction, 7, 11)
      funct3 = GrabBits(instruction, 12, 14)
      rs1 = GrabBits(instruction, 15, 19)
      rs2 = GrabBits(instruction, 20, 24)
      funct7 = GrabBits(instruction, 25, 31)
    elif opcode in self.itype:
      rd = GrabBits(instruction, 7, 11)
      funct3 = GrabBits(instruction, 12, 14)
      rs1 = GrabBits(instruction, 15, 19)
      imm = GrabBits(instruction, 20, 30) | (GrabBits(instruction, 31, 31) * 0xfffff800)
    elif opcode in self.stype:
      funct3 = GrabBits(instruction, 12, 14)
      rs1 = GrabBits(instruction, 15, 19)
      rs2 = GrabBits(instruction, 20, 24)
      imm = (GrabBits(instruction, 25, 30) << 5) | GrabBits(instruction, 7, 11) | (GrabBits(instruction, 31, 31) * 0xfffff800)
    elif opcode in self.btype:
      funct3 = GrabBits(instruction, 12, 14)
      rs1 = GrabBits(instruction, 15, 19)
      rs2 = GrabBits(instruction, 20, 24)
      imm = (GrabBits(instruction, 25, 30) << 5) | (GrabBits(instruction, 8, 11)<<1) | (GrabBits(instruction, 7, 7)<<11) | (GrabBits(instruction, 31, 31) * 0xfffff000)
    elif opcode in self.utype:
      rd = GrabBits(instruction, 7, 11)
      imm = GrabBits(instruction, 12, 31) << 12
    elif opcode in self.jtype:
      rd = GrabBits(instruction, 7, 11)
      imm = (GrabBits(instruction, 21, 30) << 1) | (GrabBits(instruction, 20, 20)<<11) | (GrabBits(instruction, 12, 19)<<12) | (GrabBits(instruction, 31, 31) * 0xfff00000)
    return opcode, rd, funct3, rs1, rs2, funct7, imm
  def execute(self):
    opcode, rd, funct3, rs1, rs2, funct7, imm = self.decode()
    if opcode == 0b0110011:
      if funct3 == 0x0:
        if funct7 == 0x0:
          self.registers[rd].set(self.registers[rs1].get() + self.registers[rs2].get()) # add
        elif funct7 == 0x20:
          self.registers[rd].set(self.registers[rs1].get() - self.registers[rs2].get()) # sub
      elif funct3 == 0x1:
        self.registers[rd].set(self.registers[rs1].get() << self.registers[rs2].get()) # sll
      elif funct3 == 0x2:
        self.registers[rd].set(1 if self.registers[rs1].gets() < self.registers[rs2].gets() else 0) # slt
      elif funct3 == 0x3:
        self.registers[rd].set(1 if self.registers[rs1] < self.registers[rs2] else 0) # sltu
      elif funct3 == 0x4:
        self.registers[rd].set(self.registers[rs1].get() ^ self.registers[rs2].get()) # xor
      elif funct3 == 0x5:
        if funct7 == 0x0:
          self.registers[rd].set(self.registers[rs1].get() >> self.registers[rs2].get()) # srl
        elif funct7 == 0x20:
          self.registers[rd].set(self.registers[rs1].gets() >> self.registers[rs2].get()) # sra