import pygame
from settings import *

class Button:
    def __init__(self, x, y, width, height, text, colour = [60, 165, 157], highlightedColour = [1, 169, 180], function = None, params = None):
        self.image = pygame.Surface([width, height])
        self.pos = [x, y]
        # returns the rect object
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.text = text
        self.font = pygame.font.SysFont("arial", width // 6)
        self.colour =colour
        self.highlightedColour = highlightedColour
        self.function = function
        self.params = params
        self.highlighed = False

    def update(self, mouse):
        self.highlighed = True if self.rect.collidepoint(mouse) else False

    def draw(self, window):
        self.image.fill(self.highlightedColour if self.highlighed else self.colour)
        window.blit(self.image, self.pos)
        font = self.font.render(self.text, False, WHITE)
        buttonWidth = self.image.get_width()
        buttonHeight = self.image.get_height()
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        pos = [self.pos[0] + (buttonWidth - fontWidth) // 2, self.pos[1] + (buttonHeight - fontHeight) // 2]
        window.blit(font, pos)

