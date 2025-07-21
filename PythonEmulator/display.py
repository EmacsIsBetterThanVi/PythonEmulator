import pygame
import os
from PythonEmulator.EmulatorCore import Ram
class Console():
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.rect = pygame.Rect(0, 0, width*8, height*16)
    self.buffer = Ram(width*height)
    self.charmap = [pygame.Surface((8, 16)) for _ in range(256)]
    self.load_charmap("default")
  def writeString(self, x, y, string):
    for i in range(len(string)):
      self.write(x+i, y, ord(string[i]))
  def write(self, x, y, char):
    self.buffer[self.width*y+x] = char
  def clear(self):
    self.buffer.wipe()
  def draw(self, screen):
    for y in range(self.height):
      for x in range(self.width):
        screen.blit(self.charmap[self.buffer[self.width*y+x]], (x*8, y*16))
  def load_charmap(self, charmap):
    image = pygame.image.load(os.path.dirname(__file__)+"/artifacts/"+charmap+".png")
    for i in range(256):
      self.charmap[i] = image.subsurface(pygame.Rect((i%16)*8, (i//16)*16, 8, 16))
  def mmioHandle(self):
    pass
  def mmio(self, address):
    return (address, self.buffer, self.mmioHandle)
