# Importing CORE, which previously was imported as using from CORE import *. This is because I am using replit and it complains about star imports. The first line is to prevent errors, while the second line is to silence the warnings.
from PyWigit import * # pyright: ignore
from PyWigit import NewScreen, SetCaption, CreateScrn, MainLoop, Screen, Status, pygame, Black, White, Windows, Button, NewFont
from PythonEmulator import Ram
from PythonEmulator.riscv import riscv32
def StartEmulator():
    EmulatorScreen.ChangeScrn(1)
    ram = Ram(65536)
    cpu = riscv32(ram)
screen = NewScreen((600, 400))
EmulatorScreen = Screen(screen, FullScreen=True)
SetCaption("Python Emulator")
# TODO: Define how each screen should look and behave
# This screen handles the main menu
font = NewFont("timesnewroman", 20)
LaunchButton = Button(font.render("Launch", True, White), LeftClick=StartEmulator)
def DrawScreen0(screen):
    LaunchButton.draw(screen, (100, 100))
def Screen0Events(event):
    return False
CreateScrn(DrawScreen0, Screen0Events, Black)
while Status():
  MainLoop(screen)
pygame.quit()