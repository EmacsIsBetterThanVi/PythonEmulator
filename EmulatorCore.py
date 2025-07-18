class register():
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
class ram():
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
      self.memory[address] = value