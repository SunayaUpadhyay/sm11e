import pygame
from settings import *
from creature import *
from projectile import *


class Player(Creature):
    game_active = True

    def __init__(
        self,
        pos,
        groups,
        obstacle_sprites,
        visible_sprites,
        damaging_objects,
        killable_sprites,
    ):
        super().__init__(groups)
        self.killable_sprites = killable_sprites
        self.visible_sprites = visible_sprites
        self.damaging_objects = damaging_objects
        self.image = pygame.image.load(
            "../graphics/player.png"
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, DEFAULT_IMAGE_SIZE)
        self.rect = self.image.get_rect(topleft=pos)
        # this basically decreases the size of the rectangle.
        # total hieght is increased by 10 pixels
        self.hitbox = self.rect.inflate(0, 10)
        self.obstacle_sprites = obstacle_sprites
        # gives (x, y) vector both of which are initialized to zero
        self.direction = pygame.math.Vector2()
        self.speed = 6
        # status of the player for animation and attacking
        self.shooting = False
        self.health = PLAYER_HEALTH
        self.shoot_timer = 150
        self.dash = False
        self.dash_time = 0
        self.can_dash = True
        self.dash_duration = 50
        self.dash_cooldown = 400
        self.shoot_time = 0
        self.invinsible = False
        self.invinsible_time = 0
        self.invinsible_countdown = 500
        self.animation_frames()
        self.animation_index = 0
        self.player_status = "right_idle"

    def animation_frames(self):
        self.animation = {
            "right": [],
            "left": [],
            "shooting": [],
            "death": [],
            "right_idle": [],
            "left_idle": [],
        }
        for i in range(8):
            anim_image_right = pygame.image.load(
                "../graphics/character/player/move/move_f" + str(i) + ".png"
            ).convert_alpha()
            anim_image_left = pygame.transform.flip(
                anim_image_right, True, False
            )
            self.animation["right"].append(
                pygame.transform.scale(anim_image_right, DEFAULT_IMAGE_SIZE)
            )
            self.animation["left"].append(
                pygame.transform.scale(anim_image_left, DEFAULT_IMAGE_SIZE)
            )
        right_idle = pygame.image.load(
            "../graphics/player.png"
        ).convert_alpha()
        right_idle = pygame.transform.scale(right_idle, DEFAULT_IMAGE_SIZE)
        self.animation["right_idle"].append(right_idle)
        self.animation["left_idle"].append(
            pygame.transform.flip(right_idle, True, False)
        )
        for i in range(2):
            anim_death = pygame.image.load(
                "../graphics/character/player/death/death_f" + str(i) + ".png"
            ).convert_alpha()
            anim_image_left = pygame.transform.flip(
                anim_image_right, True, False
            )
            self.animation["death"].append(
                pygame.transform.scale(anim_death, DEFAULT_IMAGE_SIZE)
            )

    def animate(self):
        self.get_player_state()
        self.image = self.animation[self.player_status][
            int(self.animation_index)
        ]
        self.animation_index += PLAYER_ANIMATION_TIME
        if self.animation_index >= len(self.animation[self.player_status]):
            self.animation_index = 0

    def input(self):
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y = -1
            if "right" in self.player_status:
                self.player_status = "right"
            else:
                self.player_status = "left"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            if "right" in self.player_status:
                self.player_status = "right"
            else:
                self.player_status = "left"
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.player_status = "right"
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.player_status = "left"
        else:
            self.direction.x = 0

        if mouse[0] and not self.shooting:
            self.shoot_time = pygame.time.get_ticks()
            self.shooting = True
            # self.player_status = "shooting"
            # create a new bullet which travels to the direction of the mouse
            # keep on creating new bullet as the button is mouse is clicked
            # when bullet idts
            mouse_pos = pygame.mouse.get_pos()
            Projectile(
                mouse_pos,
                self.rect,
                self.obstacle_sprites,
                self.killable_sprites,
                self.damaging_objects,
                [self.visible_sprites, self.damaging_objects],
            )

        if keys[pygame.K_LSHIFT] and self.can_dash:
            self.dash_time = pygame.time.get_ticks()
            self.dash = True
            self.can_dash = False

    def get_player_state(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.player_status:
                self.animation_index = 0
                self.player_status += "_idle"

    def player_dash(self):
        if self.dash:
            self.move(20)

    def ememy_player_collision(self):
        for sprite in self.killable_sprites:
            if pygame.sprite.collide_rect(self, sprite):
                self.damage_taken(sprite.damage)

    def damage_taken(self, damage):
        if not self.invinsible:
            self.health -= damage
            self.invinsible = True
            self.invinsible_time = pygame.time.get_ticks()
        if self.health <= 0:
            Player.game_active = False

    def update(self):
        self.input()
        self.move(self.speed)
        self.timer()
        self.get_player_state()
        self.player_dash()
        self.animate()
        self.ememy_player_collision()

    def timer(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.shoot_time > self.shoot_timer:
            self.shooting = False
        if current_time - self.dash_time > self.dash_duration:
            self.dash = False
        if current_time - self.dash_time > self.dash_cooldown:
            self.can_dash = True
        if current_time - self.invinsible_time > self.invinsible_countdown:
            self.invinsible = False
