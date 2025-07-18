class register():
  """
    A register is a variable that can be used to store a value locked to a certain size. A register can be locked to prevent it from being changed. Registers can be compared to each other and can be used in arithmetic operations, but only if they are not locked, and only for asignment operations.
  """
  def __init__(self, value=0, size=32, lock=False):
      self.value = value
      self.lock = lock
      self.max = 2**size
  def __iadd__(self, other):
      if self.lock:
          return self
      self.value += other.value
      while self.value > self.max:
          self.value -= self.max
      return self
  def __isub__(self, other):
      while self.lock:
          return self
      self.value -= other.value
      while self.value < 0:
          self.value += self.max
      return self
  def __imul__(self, other):
      if self.lock:
          return self
      self.value *= other.value
      while self.value > self.max:
          self.value -= self.max
      return self
  def __itruediv__(self, other):
      if self.lock:
          return self
      self.value //= other.value
      while self.value > self.max:
          self.value -= self.max
      return self
  def __imod__(self, other):
      if self.lock:
          return self
      self.value %= other.value
      while self.value > self.max:
          self.value -= self.max
      return self
  def __eq__(self, other):
      return self.value == other.value
  def __ne__(self, other):
      return self.value != other.value
  def __lt__(self, other):
      return self.value < other.value
  def __le__(self, other):
      return self.value <= other.value
  def __gt__(self, other):
      return self.value > other.value
  def __ge__(self, other):
      return self.value >= other.value
  def __iand__(self, other):
      if self.lock:
          return self
      self.value &= other.value
      while self.value > self.max:
          self.value -= self.max
      return self
  def __ior__(self, other):
      if self.lock:
          return self
      self.value |= other.value
      while self.value > self.max:
          self.value -= self.max
      return self
  def __ixor__(self, other):
      if self.lock:
          return self
      self.value ^= other.value
      while self.value > self.max:
          self.value -= self.max
      return self
  def __ilshift__(self, other):
      if self.lock:
          return self
      self.value <<= other.value
      while self.value > self.max:
          self.value -= self.max
      return self
  def __irshift__(self, other):
      if self.lock:
          return self
      self.value >>= other.value
      while self.value > self.max:
          self.value -= self.max
      return self
  def set(self, value):
      if self.lock:
          return self
      self.value = value
      while self.value > self.max:
          self.value -= self.max
      while self.value < 0:
          self.value += self.max
      return self.value
  def get(self):
      return self.value
class Ram():
  """
    A ram is a block of memory that can be read from and written to. It is a byte array that wraps around. It is used to store data that is not in a register. Ram can be defined to any size, but it is recommended to use a size that is a power of 2."""
  def __init__(self, size):
      self.size = size
      self.memory = bytearray(size)
  def read(self, address):
      while address < 0:
        address += self.size
      while address >= self.size:
        address-= self.size
      return self.memory[address]
  def write(self, address, value):
      while address < 0:
        address += self.size
      while address >= self.size::
        address-= self.size
      while value < 0:
        value += 256
      while value >= 256:
        value -= 256
      self.memory[address] = value