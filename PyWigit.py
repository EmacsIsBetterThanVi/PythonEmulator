import pygame
import glob
from os import getcwd
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Yellow = (255, 255, 0)
Cyan = (0, 255, 255)
Magenta = (255, 0, 255)
Gray = (128, 128, 128)
LightGray = (192, 192, 192)
DarkGray = (64, 64, 64)
Orange = (255, 128, 0)
Purple = (128, 0, 255)
Pink = (255, 0, 128)
Brown = (128, 64, 0)
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
class Pointer():
  def __init__(self, value):
    self.value = value
  def __iadd__(self, other):
    self.value += other
    return self
  def __isub__(self, other):
    self.value -= other
    return self
  def __imul__(self, other):
    self.value *= other
    return self
  def __itruediv__(self, other):
    self.value //= other
    return self
  def __imod__(self, other):
    self.value %= other
    return self
  def __iand__(self, other):
    self.value &= other
    return self
  def __ior__(self, other):
    self.value |= other
    return self
  def __ixor__(self, other):
    self.value ^= other
    return self
  def __ilshift__(self, other):
    self.value <<= other
    return self
  def __irshift__(self, other):
    self.value >>= other
    return self
  def __eq__(self, other):
    return self.value == other
  def __ne__(self, other):
    return self.value != other
  def __lt__(self, other):
    return self.value < other
  def __le__(self, other):
    return self.value <= other
  def __gt__(self, other):
    return self.value > other
  def __ge__(self, other):
    return self.value >= other
  def __add__(self, other):
    return self.value + other
  def __sub__(self, other):
    return self.value - other
  def __mul__(self, other):
    return self.value * other
  def __truediv__(self, other):
    return self.value // other
  def __mod__(self, other):
    return self.value % other
  def __and__(self, other):
    return self.value & other
  def __or__(self, other):
    return self.value | other
  def __xor__(self, other):
    return self.value ^ other
  def __lshift__(self, other):
    return self.value << other
  def __rshift__(self, other):
    return self.value >> other
  def __int__(self):
    return self.value
  def __str__(self):
    return str(self.value)
  def __repr__(self):
    return repr(self.value)
  def __hash__(self):
    return hash(self.value)
  def __bool__(self):
    return bool(self.value)
  def __len__(self):
    return len(self.value)
  def __getitem__(self, key):
    return self.value[key]
  def __setitem__(self, key, value):
    self.value[key] = value
  def __delitem__(self, key):
    del self.value[key]
  def __iter__(self):
    return iter(self.value)
  def __reversed__(self):
    return reversed(self.value)
  def __contains__(self, item):
    return item in self.value
  def __getattr__(self, name):
    return getattr(self.value, name)
  def __setattr__(self, name, value):
    if name == "value":
      self.__dict__[name] = value
    else:
      setattr(self.value, name, value)
  def __delattr__(self, name):
    delattr(self.value, name)
class Button():
    def __init__(self, display, LeftClick=None, RightClick=None, Mouse=None):
        self.display = display
        self.LeftClick=LeftClick
        self.RightClick=RightClick
        self.Mouse=Mouse
        self.rect = self.display.get_rect()
    def draw(self, screen, loc):
        self.rect = screen.blit(self.display, loc)
    def Click(self, event):
      if event.type == pygame.MOUSEBUTTONDOWN:
        if self.rect.collidepoint(event.pos):
          if event.button == 1 and self.LeftClick:
            self.LeftClick()
          elif event.button == 2 and self.RightClick:
            self.RightClick()
          elif event.button == 3 and self.Mouse:
            self.Mouse()
          return True
      return False
class ImageButton(Button):
    def __init__(self, name, LeftClick=None, RightClick=None, Mouse=None):
        self.display = pygame.image.load_extended(name)
        self.LeftClick=LeftClick
        self.RightClick=RightClick
        self.Mouse=Mouse
def NewScreen(size):
    return pygame.display.set_mode(size)
def NewFont(name, size):
    return pygame.font.SysFont(name, size)
def SetCaption(caption):
    pygame.display.set_caption(caption)
Windows = []
running = True
def CreateScrn(DrawFunc, InputFunc, color, FastTick=None):
    if FastTick:
      MultiScrn.append({"Draw":DrawFunc, "Input":InputFunc, "color":color, "FastTick":FastTick})
    else:
      MultiScrn.append({"Draw":DrawFunc, "Input":InputFunc, "color":color})
class Screen():
  def __init__(self, screen,x=0,y=0, size=(400, 400), FullScreen=False):
    self.CurentScrn = 1 # Screen starts on screen 1
    if FullScreen:
      self.screen = screen
      self.x = 0
      self.y = 0
    else:
      self.screen = pygame.Surface(size)
      self.x = x
      self.y = y
    Windows.append(self)
  def Draw(self):
    self.screen.fill(MultiScrn[self.CurentScrn]["color"])
    MultiScrn[self.CurentScrn]["Draw"](self.screen)
  def ChangeScrn(self, num):
    self.CurentScrn = num
  def Close(self):
    if len(Windows) == 1:
      global running
      running = False
    else:
      Windows.remove(self)
      del self
def Status():
    return running
class FileChoser(Screen):
  @staticmethod
  def Open(title, returnv, filetypes="*.*"):
    FileChoser(title, pygame.font.SysFont("timesnewroman", 20), returnv, filetypes)
  def __init__(self, title, font, returnv, filetypes="*.*"):
    self.title = title
    self.filetypes = filetypes
    self.file = ""
    self.font = font
    self.screen = pygame.Surface((400, 400))
    self.path = getcwd()
    self.scroll = 0
    self.x = 0
    self.y = 0
    Windows.append(self)
    self.returnv = returnv
    self.CurentScrn = 0 # FileChoser is always screen 0
    self.closeButton = Button(self.font.render("Close", True, White))
    MultiScrn[0]["Object"] = self
  def Draw(self):
    self.screen.fill(Black)
    self.closeButton.draw(self.screen, (200, 10))
    self.screen.blit(self.font.render(self.title, True, White), (10, 10))
    if self.file:
      self.screen.blit(self.font.render(self.file, True, White), (10, 40))
    self.screen.blit(self.font.render(self.path, True, White), (10, 70))
    files = glob.glob(self.path + "/" + self.filetypes)
    for i in range(len(files)):
      if i>=self.scroll and i<self.scroll+10:
        self.screen.blit(self.font.render(files[i], True, White), (10, 100 + i * 30))
  def Events(self,event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 4:
        self.scroll -= 1
      elif event.button == 5:
        self.scroll += 1
      elif event.button == 1:
        files = glob.glob(self.path + "/" + self.filetypes)
        if self.closeButton.Click(event):
          self.returnv.value = self.file
          self.Close()
          return True
        for i in range(len(files)):
          if i>=self.scroll and i<self.scroll+10:
            if pygame.Rect(10, 100 + i * 30, 400, 30).collidepoint(event.pos):
              self.file = files[i]
              return True
    return False
  @staticmethod
  def Default():
    return FileChoser("File Choser", pygame.font.SysFont("timesnewroman", 20), Pointer(""))
  def ChangeScrn(self, num):
    pass
MultiScrn = [{"Object":None, "color":White}]
FileChoser.Default()
Windows = []
FastTicks = 0
def MainLoop(screen, Fast=False):
  global running
  for event in pygame.event.get():
      handled = False
      for window in Windows:
        if MultiScrn[window.CurentScrn].get("Object"):
          handled = MultiScrn[window.CurentScrn]["Object"].Events(event)
        else:
          handled = MultiScrn[window.CurentScrn]["Input"](event)
        if handled:
          break
      if event.type == pygame.QUIT and not handled:
        running = False
  shouldTick=False
  for window in Windows:
    if MultiScrn[window.CurentScrn].get("FastTick"):
      MultiScrn[window.CurentScrn]["FastTick"]()
  if not Fast:
    shouldTick=True
  else:
    global FastTicks
    FastTicks+=1
    if FastTicks>=20:
      FastTicks=0
      shouldTick=True
  if shouldTick:
    screen.fill(Black)
    for window in Windows:
      window.Draw()
      screen.blit(window.screen, (window.x, window.y))
      pygame.draw.rect(screen, White, pygame.Rect(window.x, window.y, window.screen.get_width(), window.screen.get_height()), 1)
    pygame.display.flip()
    clock.tick(60)