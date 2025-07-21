# Importing CORE, which previously was imported as using from CORE import *. This is because I am using replit and it complains about star imports. The first line is to prevent errors, while the second line is to silence the warnings.
from PyWigit import * # pyright: ignore
from PyWigit import NewScreen, SetCaption, CreateScrn, MainLoop, Screen, Status, pygame, Black, White, Button, NewFont, FileChoser
from PythonEmulator import Ram, Memory
from PythonEmulator.display import Console
from PythonEmulator.input import Keyboard
from PythonEmulator.riscv import riscv32
cpu: riscv32=None # pyright: ignore
ram: Memory=None # pyright: ignore
console: Console=None # pyright: ignore
keyboard: Keyboard = None # pyright: ignore
RomFile: Pointer = Pointer("")
def StartEmulator():
  global ram, cpu, console, keyboard
  # Configuring the emulator
  ram = Memory([(0x00100000,Ram(2^24))], 2**32-1)
  cpu = riscv32(ram)
  console = Console(80, 25)
  keyboard = Keyboard("ascii")
  # If a rom file is specified, load it, treating it as ram, but with a locked flag set to true, so it can't be modified.
  if RomFile.value != "":
    ROM = bytearray(open(RomFile.value, "rb").read())
    ram.mm(0x0, Ram(0x10000, ROM, True))
    #for i in ROM:
    #  print(hex(i), end=" ")
    #print()
  # Our emulator will be a riscv32 emulator, with 64kb of ram, and a console with 80x25 characters
  # Because riscv uses memory mapped io, here is the memory map:
  # 0x00000000 - 0x0000FFFF: Boot ROM
  # 0x00010000 - 0x000108CF: MMIO
  #    0x00010000 - 0x0001000F: Keyboard
  #    0x00010010 - 0x0001001F: Disk
  #    0x00010040 - 0x000100FF: Reserved
  #    0x00010100 - 0x000108CF: Console
  # 0x00020000 - 0x000FFFFF: Secondary ROM
  # 0x00100000 - 0x001FFFFF: RAM
  # 0x00200000 - 0xFFFFFFFF: Reserved
  # Map the console and Keyboard to the memory map
  ram.mmio(0x10100, console)
  ram.mmio(0x10000, keyboard)
  # Change the screen to the emulator screen, starting it
  EmulatorScreen.ChangeScrn(2)
screen = NewScreen((640, 400))
EmulatorScreen = Screen(screen, FullScreen=True)
SetCaption("Python Emulator")
font = NewFont("timesnewroman", 20)
# This screen handles the main menu
LaunchButton = Button(font.render("Launch", True, White), LeftClick=StartEmulator)
SelectBootRomButton = Button(font.render("Select Boot Rom", True, White), LeftClick=lambda : FileChoser.Open("Select Boot Rom", RomFile, "*.bin"))
def DrawScreen0(screen):
    LaunchButton.draw(screen, (100, 100))
    SelectBootRomButton.draw(screen, (100, 150))
def Screen0Events(event):
    if LaunchButton.Click(event):
      return True
    if SelectBootRomButton.Click(event):
      return True
    return False
CreateScrn(DrawScreen0, Screen0Events, Black)
# This screen handles the emulator
def DrawScreen1(screen):
  console.draw(screen)
def Screen1Events(event):
  if event.type == pygame.KEYDOWN:
    if cpu.paused:
      if event.key == 32:
        x = int("0x"+input("Base Address: 0x"), 16)
        for i in range(256):
          print(f"{ram.read(x+i):02x}", end=(" " if (i+1)%16!=0 else "\n"))
      elif event.key == 113:
        EmulatorScreen.ChangeScrn(1)
    else:
      keyboard.press(event.key)
    return True
  return False
def Screen1FastTick():
  ram.mmioHandle()
  cpu.execute()
CreateScrn(DrawScreen1, Screen1Events, Black, Screen1FastTick)
while Status():
  MainLoop(screen, Fast=(ram is not None))
pygame.quit()
