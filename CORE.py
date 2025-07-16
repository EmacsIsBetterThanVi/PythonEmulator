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
CurentScrn = 0
def CreateScrn(DrawFunc, InputFunc, color):
    MultiScrn.append({"Draw":DrawFunc, "Input":InputFunc, "color":color})
running = True
def MainLoop(screen):
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            MultiScrn[CurentScrn]["Input"](event)
    screen.fill(MultiScrn[CurentScrn]["color"])
    MultiScrn[CurentScrn]["Draw"]()
    pygame.display.flip()
    clock.tick(60)
def Status():
    return running
Enter=13
Escape=27
BackSpace=8