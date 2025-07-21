def GrabBits(value, start, end):
  if end < start:
    return 0
  return (value >> start) & ((2**(end-start+1))-1)
def LittleEndian(values, size):
  result = 0
  for i in range(size):
    result |= values[i] << (i*8)
  return result
def BigEndian(values, size):
  result = 0
  for i in range(size):
    result |= values[i] << ((size-i-1)*8)
  return result
class register():
  """
    A register is a variable that can be used to store a value locked to a certain size. A register can be locked to prevent it from being changed. Registers can be compared to each other and can be used in arithmetic operations, but only if they are not locked, and only for asignment operations.
  """
  def __init__(self, value=0, size=32, lock=False):
      self.value = value
      self.lock = lock
      self.max = 2**size-1
      self.size = size
  def __iadd__(self, other):
      if self.lock:
          return self
      if isinstance(other, register):
          self.value += other.value
      else:
          self.value += other
      while self.value > self.max:
          self.value -= self.max
      return self
  def __isub__(self, other):
      while self.lock:
          return self
      if isinstance(other, register):
          self.value -= other.value
      else:
          self.value -= other
      while self.value < 0:
          self.value += self.max
      return self
  def __imul__(self, other):
      if self.lock:
          return self
      if isinstance(other, register):
          self.value *= other.value
      else:
          self.value *= other
      while self.value > self.max:
          self.value -= self.max
      return self
  def __itruediv__(self, other):
      if self.lock:
          return self
      if isinstance(other, register):
          self.value //= other.value
      else:
          self.value //= other
      while self.value > self.max:
          self.value -= self.max
      return self
  def __imod__(self, other):
      if self.lock:
          return self
      if isinstance(other, register):
          self.value %= other.value
      else:
          self.value %= other
      while self.value > self.max:
          self.value -= self.max
      return self
  def __iand__(self, other):
      if self.lock:
          return self
      if isinstance(other, register):
          self.value &= other.value
      else:
          self.value &= other
      while self.value > self.max:
          self.value -= self.max
      return self
  def __ior__(self, other):
      if self.lock:
          return self
      if isinstance(other, register):
          self.value |= other.value
      else:
          self.value |= other
      while self.value > self.max:
          self.value -= self.max
      return self
  def __ixor__(self, other):
      if self.lock:
          return self
      if isinstance(other, register):
          self.value ^= other.value
      else:
          self.value ^= other
      while self.value > self.max:
          self.value -= self.max
      return self
  def __ilshift__(self, other):
      if self.lock:
          return self
      if isinstance(other, register):
          self.value <<= other.value
      else:
          self.value <<= other
      while self.value > self.max:
          self.value -= self.max
      return self
  def __irshift__(self, other):
      if self.lock:
          return self
      if isinstance(other, register):
          self.value >>= other.value
      else:
          self.value >>= other
      while self.value > self.max:
          self.value -= self.max
      return self
  def set(self, value, Bits=(0, -1)):
      if (Bits[1] == -1):
        Bits = (Bits[0], self.size-1)
      if self.lock:
          return self
      self.value = (value & GrabBits(self.max, Bits[0], Bits[1])) | ((GrabBits(self.max, Bits[1]+1, self.size-1) << Bits[1]+1) * GrabBits(self.value, Bits[1], Bits[1]))
      while self.value > self.max:
          self.value -= self.max
      while self.value < 0:
          self.value += self.max
      return self.value
  def __eq__(self, other):
    if isinstance(other, register):
        return self.value == other.value
    else:
        return self.value == other
  def __ne__(self, other):
    if isinstance(other, register):
        return self.value != other.value
    else:
        return self.value != other
  def __lt__(self, other):
    if isinstance(other, register):
        return self.value < other.value
    else:
        return self.value < other
  def __le__(self, other):
    if isinstance(other, register):
        return self.value <= other.value
    else:
        return self.value <= other
  def __gt__(self, other):
    if isinstance(other, register):
        return self.value > other.value
    else:
        return self.value > other
  def __ge__(self, other):
    if isinstance(other, register):
        return self.value >= other.value
    else:
        return self.value >= other
  
  def __add__(self, other):
      if isinstance(other, register):
          value = self.value + other.value
      else:
          value = self.value + other
      while value > self.max:
          value -= self.max
      return value
  def __sub__(self, other):
      if isinstance(other, register):
          value = self.value - other.value
      else:
          value = self.value - other
      while value < 0:
          value += self.max
      return value
  def __mul__(self, other):
      if isinstance(other, register):
          value = self.value * other.value
      else:
          value = self.value * other
      while value > self.max:
          value -= self.max
      return value
  def __truediv__(self, other):
      if isinstance(other, register):
          value = self.value // other.value
      else:
          value = self.value // other
      while value > self.max:
          value -= self.max
      return value
  def __mod__(self, other):
      if isinstance(other, register):
          value = self.value % other.value
      else:
          value = self.value % other
      while value > self.max:
          value -= self.max
      return value
  def __and__(self, other):
      if isinstance(other, register):
          value = self.value & other.value
      else:
          value = self.value & other
      while value > self.max:
          value -= self.max
      return value
  def __or__(self, other):
      if isinstance(other, register):
          value = self.value | other.value
      else:
          value = self.value | other
      while value > self.max:
          value -= self.max
      return value
  def __xor__(self, other):
      if isinstance(other, register):
          value = self.value ^ other.value
      else:
          value = self.value ^ other
      while value > self.max:
          value -= self.max
      return value
  def __lshift__(self, other):
      if isinstance(other, register):
          value = self.value << other.value
      else:
          value = self.value << other
      while value > self.max:
          value -= self.max
      return value
  def __rshift__(self, other):
      if isinstance(other, register):
          value = self.value >> other.value
      else:
          value = self.value >> other
      while value > self.max:
          value -= self.max
      return value
  def get(self):
      return self.value
  def gets(self):
      return (self.value)-(self.max+1) if GrabBits(self.value, self.size-1, self.size-1) == 1 else self.value
class Ram():
  """
    A ram is a block of memory that can be read from and written to. It is a byte array that wraps around. It is used to store data that is not in a register. Ram can be defined to any size, but it is recommended to use a size that is a power of 2."""
  def __init__(self, size, initram=None, locked=False):
      self.memory = bytearray(size)
      if isinstance(initram, bytearray):
        for i in range(len(initram)):
          if i >= size:
            break
          self.memory[i] = initram[i]
      self.size = size
      self.locked = locked
      self.adressLimit = size
  def setAdressLimit(self, limit):
    self.adressLimit = limit
  def __getitem__(self, index):
      return self.memory[index]
  def __setitem__(self, index, value):
      self.memory[index] = value
  def wipe(self):
      self.memory = bytearray(self.size)
  def read(self, address):
      while address < 0:
        address += self.adressLimit
      while address >= self.adressLimit:
        address-= self.adressLimit
      if address >= self.size:
        return 0
      return self.memory[address]
  def write(self, address, value):
      while address < 0:
        address += self.adressLimit
      while address >= self.adressLimit:
        address-= self.adressLimit
      while value < 0:
        value += 256
      while value >= 256:
        value -= 256
      if (not self.locked) and address<self.size:
        self.memory[address] = value
class Memory():
  def __init__(self, regions=[], addressLimit=0):
    self.regions = regions
    self.addressLimit = addressLimit
    for region in self.regions:
      if region[0] + region[1].size > self.addressLimit:
        self.addressLimit = region[0] + region[1].size
  def read(self, address):
    while address > self.addressLimit:
      address-= self.addressLimit
    while address < 0:
      address += self.addressLimit
    for region in self.regions:
      if region[0] <= address < region[1].size+region[0]:
        return region[1].read(address - region[0])
    return 0
  def write(self, address, value):
    while address > self.addressLimit:
      address-= self.addressLimit
    while address < 0:
      address += self.addressLimit
    for region in self.regions:
      if region[0] <= address < region[1].size+region[0]:
        region[1].write(address - region[0], value)
        return
  def setAddressLimit(self, limit):
    self.addressLimit = limit
  def mmio(self, address, object):
    self.regions.append((object.mmio(address)))
  def mmioHandle(self):
    for region in self.regions:
      if len(region) == 3:
        region[2]()
  def mm(self, address, object):
    self.regions.append((address, object))
