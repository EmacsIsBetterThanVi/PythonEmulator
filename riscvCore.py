class hart():
  def __init__(self, ram):
      self.registers = [register(0, lock=True)]
      for i in range(31):
          self.registers.append(register())
      self.pc = register()