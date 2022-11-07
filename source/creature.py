import pygame
from settings import *
from math import *

# Parent class for player and enemies
class Creature(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

    # Manages movement
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    # Manages collission between obstacles and sprites
    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.rect.left
                    elif self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.rect.right

        elif direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.rect.top
                    elif self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.rect.bottom

    # reruns 255 or 155 based on the sin of the time
    def toggle_wave(self):
        if sin(pygame.time.get_ticks()) > 0:
            return 255
        else:
            return 155
