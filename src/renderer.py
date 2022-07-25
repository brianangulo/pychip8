import pygame

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Renderer:
    """Gluing it all together"""

    def __init__(self):
        pygame.init()
        self.size = (800, 600)
        self.running = True
        self.rows = 32
        self.columns = 64
        # creating pixel map
        self.pixel_map = self.create_screen_map()
        self.screen = pygame.display.set_mode(self.size)
        # udpating window's caption
        pygame.display.set_caption('Chip 8 Emulator')
        self.clock = pygame.time.Clock()
        self.refresh_rate = 60

    def run(self):
        self.flip_pixel(0, 0)
        self.flip_pixel(32, 16)
        self.screen_loop()

    def screen_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill(WHITE)
            # drawing pixels to the screen
            self.drawing()
            pygame.display.flip()
            self.clock.tick(self.refresh_rate)
        # exit engine once out of the loop
        pygame.quit()

    def create_screen_map(self):
        # y, x
        tmp_2d = []
        for row in range(self.rows):
            tmp_row = []
            for x in range(self.columns):
                tmp_row.append(0)
            tmp_2d.append(tmp_row)
        return tmp_2d

    def flip_pixel(self, x: int, y: int):
        pixel = self.pixel_map[y][x]
        if pixel == 0:
            self.pixel_map[y][x] = 1
        else:
            self.pixel_map[y][x] = 0

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


test = Renderer()
test.run()
