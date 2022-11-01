import pygame
from settings import *
from creature import Creature

# Enemy class
class Enemy(Creature):
    total_enemies = 0
    enemies_killed = 0

    def __init__(self, pos, type, groups, obstacle_sprites, player):
        super().__init__(groups)
        Enemy.total_enemies += 1
        self.type = type
        self.animation_frames()
        self.animation_index = 0
        self.player = player
        self.status = "right"
        self.image = self.animation[self.status][self.animation_index]
        self.obstacle_sprites = obstacle_sprites
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()
        self.data = ENEMIES[self.type]
        self.health = self.data["health"]
        self.damage = self.data["damage"]
        self.size = self.data["size"][0]
        self.speed = self.data["speed"]
        self.rect = self.rect.inflate(-self.size / 2, -self.size / 4)
        self.hitbox = self.rect.inflate(-10, -10)

    # get all the animations for the enemies
    def animation_frames(self):
        self.animation = {
            "right": [],
            "left": [],
        }
        for i in range(ENEMIES[self.type]["animation_number"]):
            graphic_location = (
                ENEMIES[self.type]["graphic"]
                + self.type
                + "_run_anim_f"
                + str(i)
                + ".png"
            )
            anim_right = pygame.image.load(graphic_location).convert_alpha()
            anim_left = pygame.transform.flip(anim_right, True, False)
            self.animation["right"].append(
                pygame.transform.scale(anim_right, ENEMIES[self.type]["size"])
            )
            self.animation["left"].append(
                pygame.transform.scale(anim_left, ENEMIES[self.type]["size"])
            )

    # get movement state for animation
    def get_state(self):
        if self.direction.x > 0:
            self.status = "right"
        else:
            self.status = "left"

    # called when ememy gets hit
    # reduces health and creates a knockback effect
    def got_hit(self, damage):
        self.health -= damage
        self.knockback()
        if self.health <= 0:
            Enemy.enemies_killed += 1
            self.kill()

    # knockback self to the opposite direction
    def knockback(self):
        opposite_direction = -self.direction
        if opposite_direction.magnitude() != 0:
            opposite_direction = opposite_direction.normalize()
        self.hitbox.x += opposite_direction.x * 10
        self.collision("horizontal")
        self.hitbox.y += opposite_direction.y * 10
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    # animate enemy graphics
    def animate(self):
        self.get_state()
        self.image = self.animation[self.status][int(self.animation_index)]
        self.animation_index += ENEMY_ANIMATION_TIME
        if self.animation_index >= len(self.animation[self.status]):
            self.animation_index = 0

    # get direction of enemy movement from the player direction
    def get_direction(self):
        target = pygame.math.Vector2(self.player.rect.center)
        current_position = pygame.math.Vector2(self.rect.center)
        self.direction = target - current_position
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

    # update all states
    def update(self):
        self.get_direction()
        self.move(self.speed)
        self.animate()
