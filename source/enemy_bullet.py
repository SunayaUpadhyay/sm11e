import pygame
from settings import *

# Projectile class enemy bullets
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(
        self,
        current_pos,
        target_pos,
        damage_player_object,
        obstacle_sprites,
        player,
        groups,
    ):
        super().__init__(groups)
        self.image = pygame.image.load("../graphics/character/enemies/bullet.png")
        self.damage_player_object = damage_player_object
        self.obstacle_sprites = obstacle_sprites
        self.current_pos = current_pos
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.direction = pygame.math.Vector2()
        self.rect = self.image.get_rect(topleft=current_pos)
        self.speed = 10
        self.player = player
        self.target_pos = target_pos
        bullet_sound = pygame.mixer.Sound("../sound/bullet2.ogg")
        bullet_sound.set_volume(0.01)
        bullet_sound.play()
        self.damage = 5
        self.get_direction()

    # get the direction of the bullet
    def get_direction(self):
        target = pygame.math.Vector2(self.target_pos)
        current_position = pygame.math.Vector2(self.current_pos)
        self.direction = target - current_position
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

    # manage interaction between the bullet and the player
    def interaction(self):
        # if bullet touches and obstacle, make it dissapear
        if pygame.sprite.spritecollideany(self, self.obstacle_sprites):
            self.kill()
        # if the bullet touched the player, make the bullet dissapear
        # and reduce health of player
        for bullet in self.damage_player_object:
            if pygame.sprite.collide_rect(bullet, self.player):
                bullet.kill()
                self.player.damage_taken(bullet.damage)

    # move the bullet
    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    # update everything
    def update(self):
        self.move()
        self.get_direction()
        self.interaction()
