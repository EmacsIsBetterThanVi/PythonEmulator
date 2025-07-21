from .EmulatorCore import Ram
class Keyboard():
  KeySets = {"PS/2-1":[{"ID": "ESC", "ScanCode": 0x01}, {"ID": "1", "ScanCode": 0x02}, {"ID": "2", "ScanCode": 0x03}, {"ID": "3", "ScanCode": 0x04}, {"ID": "4", "ScanCode": 0x05}, {"ID": "5", "ScanCode": 0x06}, {"ID": "6", "ScanCode": 0x07}, {"ID": "7", "ScanCode": 0x08}, {"ID": "8", "ScanCode": 0x09}, {"ID": "9", "ScanCode": 0x0A}, {"ID": "0", "ScanCode": 0x0B}, {"ID": "-", "ScanCode": 0x0C}, {"ID": "=", "ScanCode": 0x0D}, {"ID": "Backspace", "ScanCode": 0x0E}, {"ID": "Tab", "ScanCode": 0x0F}, {"ID": "Q", "ScanCode": 0x10}, {"ID": "W", "ScanCode": 0x11}, {"ID": "E", "ScanCode": 0x12}, {"ID": "R", "ScanCode": 0x13}, {"ID": "T", "ScanCode": 0x14}, {"ID": "Y", "ScanCode": 0x15}, {"ID": "U", "ScanCode": 0x16}, {"ID": "I", "ScanCode": 0x17}, {"ID": "O", "ScanCode": 0x18}, {"ID": "P", "ScanCode": 0x19}, {"ID": "[", "ScanCode": 0x1A}, {"ID": "]", "ScanCode": 0x1B}, {"ID": "Enter", "ScanCode": 0x1C}, {"ID": "LCtrl", "ScanCode": 0x1D}, {"ID": "A", "ScanCode": 0x1E}, {"ID": "S", "ScanCode": 0x1F}, {"ID": "D", "ScanCode": 0x20}, {"ID": "F", "ScanCode": 0x21}, {"ID": "G", "ScanCode": 0x22}, {"ID": "H", "ScanCode": 0x23}, {"ID": "J", "ScanCode": 0x24}, {"ID": "K", "ScanCode": 0x25}, {"ID": "L", "ScanCode": 0x26}, {"ID": ";", "ScanCode": 0x27}, {"ID": "'", "ScanCode": 0x28}, {"ID": "`", "ScanCode": 0x29}, {"ID": "LShift", "ScanCode": 0x2A}, {"ID": "\\", "ScanCode": 0x2B}, {"ID": "Z", "ScanCode": 0x2C}, {"ID": "X", "ScanCode": 0x2D}, {"ID": "C", "ScanCode": 0x2E}, {"ID": "V", "ScanCode": 0x2F}, {"ID": "B", "ScanCode": 0x30}, {"ID": "N", "ScanCode": 0x31}, {"ID": "M", "ScanCode": 0x32}, {"ID": ",", "ScanCode": 0x33}, {"ID": ".", "ScanCode": 0x34}, {"ID": "/", "ScanCode": 0x35}, {"ID": "RShift", "ScanCode": 0x36}, {"ID": "LAlt", "ScanCode": 0x38}, {"ID": "Space", "ScanCode": 0x39}, {"ID": "Caps Lock", "ScanCode": 0x3A}, {"ID": "F1", "ScanCode": 0x3B}, {"ID": "F2", "ScanCode": 0x3C}, {"ID": "F3", "ScanCode": 0x3D}, {"ID": "F4", "ScanCode": 0x3E}, {"ID": "F5", "ScanCode": 0x3F}, {"ID": "F6", "ScanCode": 0x40}, {"ID": "F7", "ScanCode": 0x41}, {"ID": "F8", "ScanCode": 0x42}, {"ID": "F9", "ScanCode": 0x43}, {"ID": "F10", "ScanCode": 0x44}, {"ID": "Num Lock", "ScanCode": 0x45}, {"ID": "Scroll Lock", "ScanCode": 0x46}, {"ID": "F11", "ScanCode": 0x57}, {"ID": "F12", "ScanCode": 0x58}], "ascii":[{"ID": chr(i), "CharCode": i} for i in range(65, 97)]+[{"ID": "Tab", "ScanCode": 0x09}, {"ID": "Enter", "ScanCode": 0x0A}, {"ID": "Backspace", "ScanCode": 0x08}, {"ID": "Escape", "ScanCode": 0x1B}, {"ID":"Caps Lock", "ScanCode": 0x14}, {"ID":"LShift", "ScanCode": 0x10}, {"ID":"RShift", "ScanCode": 0x11}, {"ID":"LCtrl", "ScanCode": 0x12}, {"ID":"RCtrl", "ScanCode": 0x13},{"ID":"LAlt", "ScanCode": 0x06}, {"ID":"RAlt", "ScanCode": 0x15}, {"ID":"Space", "ScanCode": 0x20},{"ID":"'", "ScanCode": 0x27}, {"ID":"`", "ScanCode": 0x60}, {"ID":"-", "ScanCode": 0x2D}, {"ID":"=", "ScanCode": 0x3D},{"ID":".", "ScanCode": 0x2E}, {"ID":",", "ScanCode": 0x2C}, {"ID":"/", "ScanCode": 0x2F}, {"ID":";", "ScanCode": 0x3B}, {"ID":"[", "ScanCode": 0x5B}, {"ID":"]", "ScanCode": 0x5D}, {"ID":"\\", "ScanCode": 0x5C}]}


  def __init__(self, Keyset="PS/2-1"):
    self.Keyset = Keyset
    self.scanCodes = self.KeySets[Keyset]
    self.pressed = [False]*len(self.scanCodes)
    self.changed = [False]*len(self.scanCodes)
    self.buffer = Ram(16)
    self.pointer = 0
  def press(self, key):
    for i in range(len(self.scanCodes)):
      if self.scanCodes[i]["ID"] == key:
        self.pressed[i] = True
        self.changed[i] = True
  def release(self, key):
    for i in range(len(self.scanCodes)):
      if self.scanCodes[i]["ID"] == key:
        self.pressed[i] = False
        self.changed[i] = True
  def get(self):
    for i in range(len(self.scanCodes)):
      if self.changed[i]:
        self.changed[i] = False
        if self.Keyset == "PS/2-1":
          if self.pressed[i]:
            return self.scanCodes[i]["ScanCode"]
          else:
            return self.scanCodes[i]["ScanCode"] | 0x80
        else:
          return self.scanCodes[i]["ScanCode"]
    return None
  def mmioHandle(self):
    x = self.get()
    if x is not None:
      self.buffer.write(self.pointer, x)
      self.pointer += 1
      if self.pointer >= 16:
        self.pointer = 0
  def mmio(self, address):
    return (address, self.buffer, self.mmioHandle)