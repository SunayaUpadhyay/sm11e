import pygame
from settings import *

# tile class for drawing tiles in the game
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surface):
        super().__init__(groups)
        self.image = surface
        self.image = pygame.transform.scale(self.image, DEFAULT_IMAGE_SIZE)
        self.rect = self.image.get_rect(topleft=pos)
