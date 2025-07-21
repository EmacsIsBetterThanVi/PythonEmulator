from .EmulatorCore import LittleEndian, register, Ram, GrabBits, Memory  
class riscv32():
  rtype = [0b0110011]
  itype = [0b0010011, 0b0000011, 0b1100111, 0b1110011]
  stype = [0b0100011]
  btype = [0b1100011]
  utype = [0b0110111, 0b0010111]
  jtype = [0b1101111]
  def __init__(self, ram):
    self.registers = [register(0, lock=True)]
    for i in range(31):
        self.registers.append(register())
    self.pc = register()
    if isinstance(ram, Ram):
      self.ram = ram
    elif isinstance(ram, Memory):
      self.ram = ram
    else:
      self.ram = Ram(ram)
    self.ram.setAddressLimit(2**32-1) # pyright: ignore
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
  # Execute the next instruction in memory
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
        self.registers[rd].set(1 if self.registers[rs1] < self.registers[rs2] else 0, (0, 0)) # slt
      elif funct3 == 0x3:
        self.registers[rd].set(1 if self.registers[rs1] < self.registers[rs2] else 0) # sltu
      elif funct3 == 0x4:
        self.registers[rd].set(self.registers[rs1].get() ^ self.registers[rs2].get()) # xor
      elif funct3 == 0x5:
        if funct7 == 0x0:
          self.registers[rd].set(self.registers[rs1].get() >> self.registers[rs2].get()) # srl
        elif funct7 == 0x20:
          self.registers[rd].set(self.registers[rs1].gets() >> self.registers[rs2].get() | (GrabBits(0xFFFFFFFF, 32 - self.registers[rs2].get(), 31) << 32 - self.registers[rs2].get()) * GrabBits(self.registers[rs1], 31, 31)) # sra
      elif funct3 == 0x6:
        self.registers[rd].set(self.registers[rs1].get() | self.registers[rs2].get()) # or
      elif funct3 == 0x7: # and
        self.registers[rd].set(self.registers[rs1].get() & self.registers[rs2].get())
    elif opcode == 0b0010011:
      if funct3 == 0x0:
        self.registers[rd].set(self.registers[rs1].get() + imm) # addi
      elif funct3 == 0x1:
        self.registers[rd].set(self.registers[rs1].get() << GrabBits(imm, 0, 4)) # slli
      elif funct3 == 0x2:
        self.registers[rd].set(1 if self.registers[rs1].gets() < imm else 0) # slti
      elif funct3 == 0x3:
        self.registers[rd].set(1 if self.registers[rs1] < imm else 0) # sltiu
      elif funct3 == 0x4:
        self.registers[rd].set(self.registers[rs1].get() ^ imm) # xori
      elif funct3 == 0x5:
        if GrabBits(imm, 5, 11) == 0x0:
          self.registers[rd].set(self.registers[rs1].get() >> GrabBits(imm, 0, 4)) # srli
        elif GrabBits(imm, 5, 11) == 0x20:
          self.registers[rd].set(self.registers[rs1].gets() >> GrabBits(imm, 0, 4) | (GrabBits(0xFFFFFFFF, 32 - GrabBits(imm, 0, 4), 31) << 32 - GrabBits(imm, 0, 4)) * GrabBits(self.registers[rs1], 31, 31)) # srai
      elif funct3 == 0x6:
        self.registers[rd].set(self.registers[rs1].get() | imm) # ori
      elif funct3 == 0x7: # andi
        self.registers[rd].set(self.registers[rs1].get() & imm)
    elif opcode == 0b0000011:
      if funct3 == 0x0:
        self.registers[rd].set(self.ram.read(self.registers[rs1].get() + imm), (0, 7)) # lb
      elif funct3 == 0x1:
        self.registers[rd].set(self.ram.read(self.registers[rs1].get() + imm) | (self.ram.read(self.registers[rs1].get() + imm + 1) << 8), (0, 15)) # lh
      elif funct3 == 0x2:
        self.registers[rd].set(self.ram.read(self.registers[rs1].get() + imm) | (self.ram.read(self.registers[rs1].get() + imm + 1) << 8) | (self.ram.read(self.registers[rs1].get() + imm + 2) << 16) | (self.ram.read(self.registers[rs1].get() + imm + 3) << 24)) # lw
      elif funct3 == 0x4:
        self.registers[rd].set(self.ram.read(self.registers[rs1].get() + imm)) # lbu
      elif funct3 == 0x5:
        self.registers[rd].set(self.ram.read(self.registers[rs1].get() + imm) | (self.ram.read(self.registers[rs1].get() + imm + 1) << 8)) # lhu
    elif opcode == 0b0100011:
      if funct3 == 0x0:
        self.ram.write(self.registers[rs1].get() + imm, GrabBits(self.registers[rs2].get(), 0, 7)) # sb
      elif funct3 == 0x1:
        self.ram.write(self.registers[rs1].get() + imm, GrabBits(self.registers[rs2].get(), 0, 7)) # sh
        self.ram.write(self.registers[rs1].get() + imm + 1, GrabBits(self.registers[rs2].get(), 8, 15)) # sh
      elif funct3 == 0x2:
        self.ram.write(self.registers[rs1].get() + imm, GrabBits(self.registers[rs2].get(), 0, 7)) # sw
        self.ram.write(self.registers[rs1].get() + imm + 1, GrabBits(self.registers[rs2].get(), 8, 15)) # sw
        self.ram.write(self.registers[rs1].get() + imm + 2, GrabBits(self.registers[rs2].get(), 16, 23)) # sw
        self.ram.write(self.registers[rs1].get() + imm + 3, GrabBits(self.registers[rs2].get(), 24, 31)) # sw
    elif opcode == 0b1100011:
      if funct3 == 0x0:
        if self.registers[rs1].get() == self.registers[rs2].get():
          self.pc.set(self.pc.get() + imm) # beq
      elif funct3 == 0x1:
        if self.registers[rs1].get() != self.registers[rs2].get():
          self.pc.set(self.pc.get() + imm) # bne
      elif funct3 == 0x4:
        if self.registers[rs1].gets() < self.registers[rs2].gets():
          self.pc.set(self.pc.get() + imm) # blt
      elif funct3 == 0x5:
        if self.registers[rs1].gets() >= self.registers[rs2].gets():
          self.pc.set(self.pc.get() + imm) # bge
      elif funct3 == 0x6:
        if self.registers[rs1].get() < self.registers[rs2].get():
          self.pc.set(self.pc.get() + imm) # bltu
      elif funct3 == 0x7:
        if self.registers[rs1].get() >= self.registers[rs2].get():
          self.pc.set(self.pc.get() + imm) # bgeu
    elif opcode == 0b1101111:
      self.registers[rd].set(self.pc.get())
      self.pc.set(self.pc.get() + imm) # jal
    elif opcode == 0b1100111:
      self.registers[rd].set(self.pc.get())
      self.pc.set(self.registers[rs1].get() + imm) # jalr
    elif opcode == 0b0110111:
      self.registers[rd].set(imm) # lui
    elif opcode == 0b0010111:
      self.registers[rd].set(self.pc.get()+imm) #auipc
    elif opcode == 0b1110011: 
      if imm == 0x0: # ecall
        pass
      elif imm == 0x1: # ebreak
        pass