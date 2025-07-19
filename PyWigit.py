import pygame
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
class Button():
    def __init__(self, display, LeftClick=None, RightClick=None, Mouse=None):
        self.display = display
        self.LeftClick=LeftClick
        self.RightClick=RightClick
        self.Mouse=Mouse
    def draw(self, screen, loc):
        screen.blit(self.display, loc)
    def Click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.display.collidepoint(event.pos):
                if event.button == 1 and self.LeftClick:
                    self.LeftClick()
                elif event.button == 2 and self.RightClick:
                    self.RightClick()
                elif event.button == 3 and self.Mouse:
                    self.Mouse()
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
MultiScrn = []
Windows = []
running = True
def CreateScrn(DrawFunc, InputFunc, color):
    MultiScrn.append({"Draw":DrawFunc, "Input":InputFunc, "color":color})
class Screen():
  def __init__(self, screen,x=0,y=0, size=(400, 400), FullScreen=False):
    self.CurentScrn = 0
    if FullScreen:
      self.screen = screen
      self.x = 0
      self.y = 0
    else:
      self.screen = pygame.Surface(size)
      self.x = x
      self.y = y
    Windows.append(self)
  def MainLoop(self):
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
Enter=13
Escape=27
BackSpace=8
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
def MainLoop(screen):
  global running
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      else:
        handled = False
        for window in Windows:
          handled = MultiScrn[window.CurentScrn]["Input"](event)
          if handled:
            break
  screen.fill(Black)
  for window in Windows:
    window.MainLoop()
    screen.blit(window.screen, (window.x, window.y))
  pygame.display.flip()
  clock.tick(60)