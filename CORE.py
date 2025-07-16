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
    def draw(screen, loc):
        screen.blit(display, loc)
    def Click(event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if display.collidepoint(event.pos):
                if event.button == 1:
                    self.LeftClick()
                elif event.button == 2:
                    self.RightClick()
                elif event.button == 3:
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
def MainLoop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            MultiScrn[CurentScrn]["Input"](event)
    screen.fill(MultiScrn[CurentScrn]["color"])
    MultiScrn[CurentScrn]["Draw"]()
    pygame.display.flip()
    clock.tick(60)
Enter=13
Escape=27
BackSpace=8