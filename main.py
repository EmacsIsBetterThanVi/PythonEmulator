# Importing CORE, which previously was imported as using from CORE import *. This is because I am using replit and it complains about star imports. The first line is to prevent errors, while the second line is to silence the warnings.
from PyWigit import * # pyright: ignore
from PyWigit import NewScreen, SetCaption, CreateScrn, MainLoop, Screen, Status, pygame, Black, White, Button, NewFont, FileChoser, DropDown
from PythonEmulator import Ram, Memory, Serial
from PythonEmulator.display import Console
from PythonEmulator.input import Keyboard
from PythonEmulator.riscv import riscv32
cpu: riscv32=None # pyright: ignore
ram: Memory=None # pyright: ignore
console: Console=None # pyright: ignore
keyboard: Keyboard = None # pyright: ignore
RomFile: Pointer = Pointer("")
MemoryMap: str = "riscvgeneric"
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
    #for i in ROM:
    #  print(hex(i), end=" ")
    #print()
  else:
    ROM = bytearray()
  # Because riscv uses memory mapped io, here are the memory maps:
  # riscvgeneric:
  # 0x00000000 - 0x0000FFFF: Boot ROM
  # 0x00010000 - 0x000108CF: MMIO
  #    0x00010000 - 0x0001000F: Keyboard
  #    0x00010010 - 0x0001001F: Disk
  #    0x00010040 - 0x000100F7: Reserved
  #    0x000100F8 - 0x000100FB: ECALL
  #    0x000100FC - 0x000100FF: EBREAK
  #    0x00010100 - 0x000108CF: Console
  # 0x00020000 - 0x000FFFFF: Secondary ROM
  # 0x00100000 - 0x001FFFFF: RAM
  # 0x00100000 - 0x001FFFFF: Stack(SP set to 0x001FFFFF)
  # 0x00220000 - 0xFFFFFFFF: Reserved
  # riscvqemu:
  # 0x80000000 - 0x87FFFFFF: Boot Rom
  # 0x20000000 - 0x21FFFFFF: Flash 1
  # 0x22000000 - 0x23FFFFFF: Flash 2
  # 0x10000000 - 0x10000007: Serial Ports
  # 0x80000000 - 0x87FFFFFF: Ram
  # 0x80000000 - 0x87FFFFFF: Stack(SP set to 0x87FFFFFF)
  # 0x00101000 - 0x00101024: RTC
  # It should be noted that the Stack grows upwards in 16 byte blocks 
  if MemoryMap == "riscvgeneric":
    ram.mm(0x0, Ram(0x10000, ROM, True))
    # Map the console and Keyboard to the memory map
    ram.mmio(0x10100, console)
    ram.mmio(0x10000, keyboard)
  elif MemoryMap == "riscvqemu":
    cpu.registers[2].value = 0x87FFFFFF
    ram.mm(0x80000000, Ram(0x8000000, ROM))
    Serial(console, ram, 0x10000000)
    Serial(keyboard, ram, 0x10000001)
  # Change the screen to the emulator screen, starting it
  EmulatorScreen.ChangeScrn(2)
screen = NewScreen((640, 400))
EmulatorScreen = Screen(screen, FullScreen=True)
SetCaption("Python Emulator")
font = NewFont("timesnewroman", 20)
# This screen handles the main menu
MemoryMaps: DropDown = DropDown(["Generic Risc-V Memory Mapping", "Qemu Risc-V Memory Mapping"], ["riscvgeneric", "riscvqemu"],font)
LaunchButton = Button(font.render("Launch", True, White), LeftClick=StartEmulator)
SelectBootRomButton = Button(font.render("Select Boot Rom", True, White), LeftClick=lambda : FileChoser.Open("Select Boot Rom", RomFile, "*.bin"))
def DrawScreen0(screen):
    LaunchButton.draw(screen, (100, 20))
    SelectBootRomButton.draw(screen, (100, 50))
    MemoryMaps.draw(screen, (100, 80))
def Screen0Events(event):
    if LaunchButton.Click(event):
      return True
    if SelectBootRomButton.Click(event):
      return True
    if MemoryMaps.Click(event):
      return True
    return False
CreateScrn(DrawScreen0, Screen0Events, Black)
# This screen handles the emulator
def DrawScreen1(screen):
  console.draw(screen)
def Screen1Events(event):
  if event.type == pygame.KEYDOWN:
    if cpu.paused:
      if event.key == 109:
        x = int("0x"+input("Base Address: 0x"), 16)
        for i in range(256):
          print(f"{ram.read(x+i):02x}", end=(" " if (i+1)%16!=0 else "\n"))
      elif event.key == 113:
        EmulatorScreen.ChangeScrn(1)
      elif event.key == 115:
        cpu.step = not cpu.step
        print(f"Single step mode {'' if cpu.step else 'de'}activated.")
      elif event.key == 114:
        cpu.reset()
      elif event.key == 32:
        cpu.paused = False
      else:
        print(event.key)
    else:
      keyboard.press(event.key)
    return True
  return False
def Screen1FastTick():
  ram.mmioHandle()
  if MemoryMap == "riscvgeneric":
    cpu.ramregister(0x000100F8, "ecall")
    cpu.ramregister(0x000100FC, "ebreak")
  elif MemoryMap == "riscvqemu":
    pass
  cpu.execute()
CreateScrn(DrawScreen1, Screen1Events, Black, Screen1FastTick)
while Status():
  MainLoop(screen, Fast=(ram is not None))
pygame.quit()
