import pygame
import sys
from keyboard import Keyboard
from cpu import CPU
from memory import memory
from toolbar import Toolbar
from filedialog import Filedialog

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Renderer:
    """Gluing it all together"""

    def __init__(self):
        # this must be instantiated before pygame.init()
        # it prevents SDL crashes when using tkinter by embedding the windows
        self.filedialog = Filedialog()
        pygame.init()
        pygame.mixer.init()
        self.beep = pygame.mixer.Sound('assets/beep.wav')
        self.keyboard = Keyboard(pygame)
        self.memory = memory()
        self.cpu = CPU(self.memory, self, self.keyboard)
        self.size = (800, 650)
        self.running = True
        self.rows = 32
        self.columns = 64
        # creating pixel map
        self.pixel_map = self.create_screen_map()
        self.screen = pygame.display.set_mode(self.size)
        # updating window's caption
        pygame.display.set_caption('Chip 8 Emulator')
        self.clock = pygame.time.Clock()
        self.refresh_rate = 60
        self.toolbar = Toolbar(self.size[0], 50, self.load_rom, pygame)

    def load_rom(self):
        # grab a file through tkinter
        self.filedialog.launch()
        if self.filedialog.file:
            # clear screen
            self.clear_pixels()
            # clear VM memory
            self.memory = memory()
            # restart cpu with a new file
            self.cpu = CPU(self.memory, self, self.keyboard, self.filedialog.file)

    def run(self):
        self.screen_loop()

    def screen_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill(WHITE)
            self.keyboard.set_pressed(pygame.key.get_pressed())
            self.cpu.cycle()
            # drawing pixels to the screen
            self.drawing()
            self.toolbar.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.refresh_rate)
        # exit engine once out of the loop
        pygame.quit()
        sys.exit()

    def control_beep(self, play: bool):
        if play:
            self.beep.play()
        else:
            self.beep.stop()

    def create_screen_map(self):
        # y, x
        tmp_2d = []
        for row in range(self.rows):
            tmp_row = []
            for x in range(self.columns):
                tmp_row.append(0)
            tmp_2d.append(tmp_row)
        return tmp_2d

    def set_pixel(self, x: int, y: int, bit: int):
        pixel = self.pixel_map[y][x]
        self.pixel_map[y][x] = self.pixel_map[y][x] ^ bit
        if pixel == 1 and self.pixel_map[y][x] == 0:
            return True
        else:
            return False

    def clear_pixels(self):
        self.pixel_map = self.create_screen_map()

    def drawing(self):
        for index, row in enumerate(self.pixel_map):
            for idx, column in enumerate(row):
                step = 10
                offset = 80
                pixel = pygame.Rect(step * idx + offset,
                                    index * step + offset, 10, 10)
                color = WHITE if column == 0 else BLACK
                pygame.draw.rect(self.screen, color, pixel)

    def handle_quit(self):
        if self.running:
            self.running = False
