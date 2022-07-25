from renderer import Renderer
from keyboard import Keyboard

class CPU:
    def __init__(self, memory: bytearray, renderer: Renderer, keyboard: Keyboard):
        self.renderer = renderer
        self.memory = memory
        self.keyboard = keyboard
        # general purpose registers where x is a hexadecimal digit (0 through F)
        # VF register should not be used by any program, as it is used as a flag by some instructions
        self.V = bytearray(16)
        # 16bit memory address holder register
        self.I = 0
        # This timer does nothing more than subtract 1 from the value of DT at a rate of 60Hz.
        self.DT = 0
        # ST timer also decrements at a rate of 60Hz as long as ST's value is > 0 CHIP8 will buzz
        self.ST = 0
        # pseudo registers
        self.SP = 0  # stack pointer this we may not need to use
        self.PC = 0x200  # program counter
        # subroutine return adresses stack
        self.stack = [0] * 16
    
    def run_timers(self):
        # delay timer
        if self.DT != 0:
            self.DT -= 1
        # sound timer
        if self.ST != 0:
            self.ST -= 1
            # play beep?
            self.renderer.play_beep()