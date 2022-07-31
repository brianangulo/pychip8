from renderer import Renderer
from keyboard import Keyboard
from sprites import sprites
from random import randint


class CPU:
    def __init__(self, memory: bytearray, renderer: Renderer, keyboard: Keyboard):
        self.renderer = renderer
        self.memory = memory
        self.keyboard = keyboard
        self.is_paused = False
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
        self.SP = -1  # stack pointer treating it as a 16 bit
        self.PC = 0x200  # program counter
        # subroutine return adresses stack
        self.stack = []
        # loading sprites should run after memory has been initialized
        self.load_sprites()

    def run_timers(self):
        # delay timer
        if self.DT != 0:
            self.DT -= 1
        # sound timer
        if self.ST != 0:
            self.renderer.play_beep()
            # play beep?
            self.ST -= 1

    def load_sprites(self):
        mem_idx = 0
        for sprite in sprites:
            for byte in sprites[sprite]:
                self.memory[mem_idx] = byte
                # count up memory index
                mem_idx += 1

    def fetch_instructions(self):
        # TODO: create instruction fetching logic
        # incrementing counter by 2 as each instruction is 2 bytes long
        self.PC += 2

    def run_instruction(self, instruction: int):
        # instructions are 16 bits long
        # below extracts the key, high nibble of the high byte
        key = (instruction & 0xF000) >> 12
        # further decoding splitting into reusable variables
        # extracting needed bits from the instruction
        x = (instruction & 0x0F00) >> 8
        y = (instruction & 0x00F0) >> 4
        nnn = instruction & 0x0FFF
        # nibble
        n = instruction & 0x000F
        kk = instruction & 0x00FF

        if key == 0x0000:
            # non key instructions
            if instruction == 0x00E0:
                # 00E0 - CLS
                # Clear the display.
                self.renderer.clear_screen()
            elif instruction == 0x00EE:
                # 00EE - RET
                # Return from a subroutine.
                # The interpreter sets the program counter to the address at the top of the stack,
                # then subtracts 1 from the stack pointer.
                self.PC = self.stack[self.SP]
                self.SP -= 1
        elif key == 0x1:
            # 1nnn - JP addr
            # Jump to location nnn.
            # The interpreter sets the program counter to nnn.
            self.PC = nnn
        elif key == 0x2:
            # 2nnn - CALL addr
            # Call subroutine at nnn.
            # The interpreter increments the stack pointer,
            # then puts the current PC on the top of the stack. The PC is then set to nnn.
            self.SP += 1
            self.stack.append(self.PC)
            self.PC = nnn
        elif key == 0x3:
            # 3xkk - SE Vx, byte
            # Skip next instruction if Vx = kk.
            # The interpreter compares register Vx to kk,
            # and if they are equal, increments the program counter by 2
            if self.V[x] == kk:
                self.PC += 2
        elif key == 0x4:
            # 4xkk - SNE Vx, byte
            # Skip next instruction if Vx != kk.
            # The interpreter compares register Vx to kk,
            # and if they are not equal, increments the program counter by 2.
            if self.V[x] != kk:
                self.PC += 2
        elif key == 0x5:
            # 5xy0 - SE Vx, Vy
            # Skip next instruction if Vx = Vy.
            # The interpreter compares register Vx to register Vy,
            # and if they are equal, increments the program counter by 2.
            if self.V[x] == self.V[y]:
                self.PC += 2
        elif key == 0x6:
            # 6xkk - LD Vx, byte
            # Set Vx = kk.
            # The interpreter puts the value kk into register Vx.
            self.V[x] = kk
        elif key == 0x7:
            # 7xkk - ADD Vx, byte
            # Set Vx = Vx + kk.
            # Adds the value kk to the value of register Vx, then stores the result in Vx.
            self.V[x] = self.V[x] + kk
        elif key == 0x8:
            # further decoding and executing 8s
            key_8 = instruction & 0x000F
            if key_8 == 0x0:
                # 8xy0 - LD Vx, Vy
                # Set Vx = Vy.
                # Stores the value of register Vy in register Vx.
                self.V[x] = self.V[y]
            elif key_8 == 0x1:
                # 8xy1 - OR Vx, Vy
                # Set Vx = Vx OR Vy.
                # Performs a bitwise OR on the values of Vx and Vy,
                # then stores the result in Vx.
                self.V[x] = self.V[x] | self.V[y]
            elif key_8 == 0x2:
                # 8xy2 - AND Vx, Vy
                # Set Vx = Vx AND Vy.
                # Performs a bitwise AND on the values of Vx and Vy,
                # then stores the result in Vx.
                self.V[x] = self.V[x] & self.V[y]
            elif key_8 == 0x3:
                # 8xy3 - XOR Vx, Vy
                # Set Vx = Vx XOR Vy.
                # Performs a bitwise exclusive OR on the values of Vx and Vy,
                # then stores the result in Vx.
                self.V[x] = self.V[x] ^ self.V[y]
            elif key_8 == 0x4:
                # 8xy4 - ADD Vx, Vy
                # Set Vx = Vx + Vy, set VF = carry.
                # The values of Vx and Vy are added together.
                # If the result is greater than 8 bits (i.e., > 255,) VF is set to 1, otherwise 0.
                # Only the lowest 8 bits of the result are kept, and stored in Vx.
                sum_xy = self.V[x] + self.V[y]
                if sum_xy > 0xFF:
                    self.V[0xF] = 0x1
                else:
                    self.V[0xF] = 0x0
                self.V[x] = sum_xy & 0x00FF
            elif key_8 == 0x5:
                # 8xy5 - SUB Vx, Vy
                # Set Vx = Vx - Vy, set VF = NOT borrow.
                # If Vx > Vy, then VF is set to 1, otherwise 0.
                # Then Vy is subtracted from Vx, and the results stored in Vx.
                if self.V[x] > self.V[y]:
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0
                self.V[x] = self.V[x] - self.V[y]
            elif key_8 == 0x6:
                # 8xy6 - SHR Vx {, Vy}
                # Set Vx = Vx SHR 1.
                # If the least-significant bit of Vx is 1,
                # then VF is set to 1, otherwise 0. Then Vx is divided by 2.
                self.V[0xF] = self.V[x] & 0x1
                # hacky divide by 2
                self.V[x] = self.V[x] >> 1
            elif key_8 == 0x7:
                # 8xy7 - SUBN Vx, Vy
                # Set Vx = Vy - Vx, set VF = NOT borrow.
                # If Vy > Vx, then VF is set to 1, otherwise 0.
                # Then Vx is subtracted from Vy, and the results stored in Vx.
                if self.V[y] > self.V[x]:
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0
                self.V[x] = self.V[y] - self.V[x]
            elif key_8 == 0xE:
                # 8xyE - SHL Vx {, Vy}
                # Set Vx = Vx SHL 1.
                # If the most-significant bit of Vx is 1,
                # then VF is set to 1, otherwise to 0. Then Vx is multiplied by 2.
                self.V[0xF] = self.V[x] & 0x80
                # hacky *2
                self.V[x] = self.V[x] << 1
        elif key == 0x9:
            # 9xy0 - SNE Vx, Vy
            # Skip next instruction if Vx != Vy.
            # The values of Vx and Vy are compared,
            # and if they are not equal, the program counter is increased by 2.
            if self.V[x] != self.V[y]:
                self.PC += 2
        elif key == 0xA:
            # Annn - LD I, addr
            # Set I = nnn.
            # The value of register I is set to nnn.
            self.I = nnn
        elif key == 0xB:
            # Bnnn - JP V0, addr
            # Jump to location nnn + V0.
            # The program counter is set to nnn plus the value of V0.
            self.PC = nnn + self.V[0]
        elif key == 0xC:
            # Cxkk - RND Vx, byte
            # Set Vx = random byte AND kk.
            # The interpreter generates a random number from 0 to 255,
            # which is then ANDed with the value kk.
            # The results are stored in Vx.
            random_num = randint(0, 255)
            self.V[x] = random_num & kk
        elif key == 0xD:
            # Dxyn - DRW Vx, Vy, nibble
            # Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision.
            # The interpreter reads n bytes from memory, starting at the address stored in I.
            # These bytes are then displayed as sprites on screen at coordinates (Vx, Vy).
            # Sprites are XORed onto the existing screen.
            # If this causes any pixels to be erased, VF is set to 1,
            # otherwise it is set to 0.
            # If the sprite is positioned so part of it is outside the coordinates of the display,
            # it wraps around to the opposite side of the screen.
            n_idx = 0
            sprite = []
            # reading sprite data from memory
            while n_idx < n:
                sprite.append(self.memory[self.I + n_idx])
                n_idx += 1
            # starting mask
            mask = 0x80
            # 2d array will hold sprite data
            sprite_map = []
            for byte in sprite:
                idx = 0
                # 1d array for each sprite row
                sprite_row = []
                while idx < 8:
                    # reading single bit values from the sprite byte and adding them to the row
                    sprite_row.append((byte & (mask >> idx)) >> (7 - idx))
                    idx += 1
                # adding rows to the map
                sprite_map.append(sprite_row)
            # painting the sprite map to the screen
            collisions = []
            for idx_y, row in enumerate(sprite_map):
                for idx_x, bit in enumerate(row):
                    # accounting for wrapping starting behavior for x and y
                    xx = self.V[x] & (self.renderer.columns - 1)
                    yy = self.V[y] & (self.renderer.rows - 1)
                    collided = self.renderer.set_pixel(
                        xx + idx_x, yy + idx_y, bit)
                    collisions.append(collided)
            # checking for collisions
            if any(collisions):
                self.V[0xF] = 1
            else:
                self.V[0xF] = 0

        elif key == 0xE:
            # keyboard instructions
            # TODO: finalize keyboard logic
            key_e = instruction & 0x000F
            if key_e == 0xE:
                # Ex9E - SKP Vx
                # Skip next instruction if key with the value of Vx is pressed.
                # Checks the keyboard, and if the key corresponding to the value of Vx
                # is currently in the down position, PC is increased by 2.
                pass
            elif key_e == 0x1:
                # ExA1 - SKNP Vx
                # Skip next instruction if key with the value of Vx is not pressed.
                # Checks the keyboard, and if the key corresponding
                # to the value of Vx is currently in the up position, PC is increased by 2.
                pass
        elif key == 0xF:
            key_f = instruction & 0x000F
            if key_f == 0x7:
                # Fx07 - LD Vx, DT
                # Set Vx = delay timer value.
                # The value of DT is placed into Vx.
                self.V[x] = self.DT
            elif key_f == 0xA:
                # Fx0A - LD Vx, K
                # Wait for a key press, store the value of the key in Vx.
                # All execution stops until a key is pressed,
                # then the value of that key is stored in Vx.
                pass
            elif key_f == 0x5:
                # Fx15 - LD DT, Vx
                # Set delay timer = Vx.
                # DT is set equal to the value of Vx.
                self.DT = self.V[x]
            elif key_f == 0x8:
                # Fx18 - LD ST, Vx
                # Set sound timer = Vx.
                # ST is set equal to the value of Vx.
                self.ST = self.V[x]
            elif key_f == 0xE:
                # Fx1E - ADD I, Vx
                # Set I = I + Vx.
                # The values of I and Vx are added, and the results are stored in I.
                self.I = self.I + self.V[x]
            elif key_f == 0x9:
                # Fx29 - LD F, Vx
                # Set I = location of sprite for digit Vx.
                # The value of I is set to the location for the hexadecimal
                # sprite corresponding to the value of Vx. See section 2.4, Display, for more information on the Chip-8 hexadecimal font.
                self.I = (self.V[x] & 0x0F) * 5
            elif key_f == 0x3:
                # Fx33 - LD B, Vx
                # Store BCD representation of Vx in memory locations I, I+1, and I+2.
                # The interpreter takes the decimal value of Vx,
                # and places the hundreds digit in memory at location in I, the tens digit at location I+1, and the ones digit at location I+2.
                self.memory[self.I] = int(self.V[x] / 100)
                self.memory[self.I + 1] = int((self.V[x] % 100) / 10)
                self.memory[self.I + 2] = int(self.V[x] % 10)
            elif key_f == 0x5:
                key_f5 = instruction & 0x00FF
                if key_f5 == 0x55:
                    # Fx55 - LD [I], Vx
                    # Store registers V0 through Vx in memory starting at location I.
                    # The interpreter copies the values of registers V0 through Vx into memory, starting at the address in I.
                    idx = 0
                    while idx < x:
                        self.memory[self.I + idx] = self.V[idx]
                        idx += 1
                elif key_f5 == 0x65:
                    # Fx65 - LD Vx, [I]
                    # Read registers V0 through Vx from memory starting at location I.
                    # The interpreter reads values from memory starting at location I into registers V0 through Vx.
                    idx = 0
                    while idx < x:
                        self.V[idx] = self.memory[self.I + idx]
                        idx += 1
