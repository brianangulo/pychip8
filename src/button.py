from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pygame

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Button:
    def __init__(self, color, x, y, width, height, pygame_instance: pygame, text=''):
        self.default_color = color
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.pygame = pygame_instance

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        self.mouseover_update_color()
        self.on_click()
        if outline:
            self.pygame.draw.rect(
                win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        self.pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            default_font = self.pygame.font.get_default_font()
            font = self.pygame.font.SysFont(default_font, 30)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                            self.y + (self.height / 2 - text.get_height() / 2)))

    def mouseover_update_color(self):
        # updates the color as needed to act change effect when mouse over
        if self.is_over(self.pygame.mouse.get_pos()):
            self.color = RED
        elif not self.is_over(self.pygame.mouse.get_pos()) and self.color == RED:
            self.color = self.default_color

    def on_click(self):
        mouse_buttons = self.pygame.mouse.get_pressed()
        if mouse_buttons[0] and self.is_over(self.pygame.mouse.get_pos()):
            return True

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False
