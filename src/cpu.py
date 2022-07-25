class CPU:
    def __init__(self, memory, renderer):
        self.renderer = renderer
        self.memory = memory
        # general purpose registers
        self.v = bytearray(16)
        # 16bit memory address holder register
        self.I = 0
        # timers and sounds special purpose registers
        self.delayTimer = 0
        self.soundTimer = 0
        # pseudo registers
        self.sp = 0 # stack pointer this we may not need to use
        self.pc = 0x200 # program counter
        # call stack
        self.stack = []