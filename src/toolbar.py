from button import Button

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# it should accomadate multiple buttons and handlers in the future


class Toolbar:
    def __init__(self, width, height, button_handler, pygame):

        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.leftbutton = Button(
            WHITE, 5, 5, 130, height - 10, pygame, 'Load ROM')
        self.button_handler = button_handler
        self.pygame = pygame

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.leftbutton.draw(screen)
        if self.leftbutton.isOver(self.pygame.mouse.get_pos()):
            self.button_handler()
