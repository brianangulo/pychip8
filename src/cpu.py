class CPU:
    def __init__(self) -> None:
        self.memory = bytearray(4096)
        # general purpose registers
        self.v = bytearray(16)
        # 16bit memory address holder register
        self.I = bytearray(2)
        # timers and sounds special purpose registers
        self.sr = bytearray(1)
        self.sr2 = bytearray(1)