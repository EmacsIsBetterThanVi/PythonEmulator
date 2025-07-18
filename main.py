# Importing CORE, which previously was imported as using from CORE import *. This is because I am using replit and it complains about star imports. The first line is to prevent errors, while the second line is to silence the warnings.
from CORE import * # pyright: ignore
from CORE import NewScreen, SetCaption, CreateScrn, MainLoop,  Status, pygame, Black

# TODO: Define Screen size, and Game Name
screen = NewScreen((400, 400))
SetCaption("Game")
# TODO: Define how each screen should look and behave
# This screen handles the 
def DrawScreen0():
    pass
def Screen0Events(event):
    pass
CreateScrn(DrawScreen0, Screen0Events, Black)
# If we need more screens, just duplicate this section and change the numbers to the next number in the sequence
while Status():
  MainLoop(screen)
pygame.quit()