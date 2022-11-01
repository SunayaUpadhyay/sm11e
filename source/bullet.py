import pygame
from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, groups, target_pos):
        super().__init__(groups)
        self.target_pos = target_pos
        self.image = pygame.image.load("graphics/tile32.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        # gives (x, y) vector both of which are initialized to zero
        self.speed = 8

    def update(self):
        self.move(self.speed)

    def move(self, speed):
        slope = self.target_pos[0] // self.target_pos[1]
        self.rect.x += self.target_pos[0] / 1000 * speed
        self.rect.y += self.target_pos[1] / 1000 * speed
