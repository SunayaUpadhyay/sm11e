import pygame
from settings import *

# Projectile class for gun bullets
class Projectile(pygame.sprite.Sprite):
    def __init__(
        self,
        target_pos,
        rect_pos,
        obstacle_sprites,
        killable_sprites,
        damaging_objects,
        groups,
    ):
        super().__init__(groups)
        self.damaging_objects = damaging_objects
        self.obstacle_sprites = obstacle_sprites
        self.killable_sprites = killable_sprites
        self.image = pygame.image.load(
            "../graphics/character/player/bullet/bullet_f0.png"
        )
        self.came_from = "player"
        self.image = pygame.transform.scale(self.image, (24, 24))
        self.direction = pygame.math.Vector2()
        self.rect = self.image.get_rect(center=rect_pos.center)
        self.hitbox = self.rect.inflate(-10, -10)
        self.speed = 15
        background_sound = pygame.mixer.Sound("../sound/bullet.wav")
        background_sound.set_volume(0.01)
        background_sound.play()
        self.damage = BULLET_DATA["damage"]
        self.target_pos = target_pos
        self.get_direction()

    # get the direction of the bullet
    def get_direction(self):
        target = pygame.math.Vector2(self.target_pos)
        current_position = pygame.math.Vector2((WIDTH / 2, HEIGHT / 2))
        self.direction = target - current_position
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

    # manage interaction between the bullet and the sprite
    def interaction(self):
        if pygame.sprite.spritecollideany(self, self.obstacle_sprites):
            self.kill()
        # loop through all the killable and damaging objects and check for collisions
        # if there is a collission between the bullet and a killable sprite, remove the
        # bullet from the screen, and call the got_hit function for the killable sprite
        # the got_hit function should call the knockback funciton and damage function
        # the damagae function should kill the object if it's health is 0
        for bullet in self.damaging_objects:
            for sprite in self.killable_sprites:
                if pygame.sprite.collide_rect(bullet, sprite):
                    bullet.kill()
                    sprite.got_hit(bullet.damage)

    # move the bullet
    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * self.speed
        self.hitbox.y += self.direction.y * self.speed
        self.rect.center = self.hitbox.center

    # update everything
    def update(self):
        self.move()
        self.interaction()
