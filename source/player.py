import pygame
from settings import *
from creature import *
from projectile import *
import math

# player class
class Player(Creature):
    game_active = True
    # initialize the player
    def __init__(
        self,
        pos,
        groups,
        obstacle_sprites,
        visible_sprites,
        damaging_objects,
        killable_sprites,
        damage_player_object,
    ):
        super().__init__(groups)
        self.killable_sprites = killable_sprites
        self.visible_sprites = visible_sprites
        self.damage_player_object = damage_player_object
        self.damaging_objects = damaging_objects
        self.display_surface = pygame.display.get_surface()
        self.image = pygame.image.load(
            "../graphics/character/player/move/move_f1.png"
        ).convert_alpha()
        self.gun = pygame.image.load("../graphics/wepons/AK47/AK47.png").convert_alpha()
        self.gun = pygame.transform.flip(self.gun, True, False)
        self.gun = pygame.transform.scale(self.gun, (60, 60))
        self.image = pygame.transform.scale(self.image, PLAYER_DEFAULT_IMAGE_SIZE)
        self.rect = self.image.get_rect(topleft=pos)
        self.moved = False
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
        self.dash_duration = 60
        self.dash_cooldown = 1000
        self.shoot_time = 0
        self.invinsible = False
        self.invinsible_time = 0
        self.invinsible_countdown = 500
        self.animation_frames()
        self.animation_index = 0
        self.player_status = "right_idle"

    # all the animation frames of the player
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
            anim_image_left = pygame.transform.flip(anim_image_right, True, False)
            self.animation["right"].append(
                pygame.transform.scale(anim_image_right, PLAYER_DEFAULT_IMAGE_SIZE)
            )
            self.animation["left"].append(
                pygame.transform.scale(anim_image_left, PLAYER_DEFAULT_IMAGE_SIZE)
            )
        right_idle = pygame.image.load(
            "../graphics/character/player/move/move_f1.png"
        ).convert_alpha()
        right_idle = pygame.transform.scale(right_idle, PLAYER_DEFAULT_IMAGE_SIZE)
        self.animation["right_idle"].append(right_idle)
        self.animation["left_idle"].append(
            pygame.transform.flip(right_idle, True, False)
        )
        for i in range(2):
            anim_death = pygame.image.load(
                "../graphics/character/player/death/death_f" + str(i) + ".png"
            ).convert_alpha()
            anim_image_left = pygame.transform.flip(anim_image_right, True, False)
            self.animation["death"].append(
                pygame.transform.scale(anim_death, PLAYER_DEFAULT_IMAGE_SIZE)
            )

    # animate the player
    def animate(self):
        self.get_player_state()
        self.image = self.animation[self.player_status][int(self.animation_index)]
        self.animation_index += PLAYER_ANIMATION_TIME
        if self.animation_index >= len(self.animation[self.player_status]):
            self.animation_index = 0
        if self.invinsible:
            self.image.set_alpha(self.toggle_wave())
        else:
            self.image.set_alpha(255)

    # get input from the player
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

        if self.direction.magnitude() > 0:
            self.moved = True

    # get player state for animation frames
    def get_player_state(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.player_status:
                self.animation_index = 0
                self.player_status += "_idle"

    # player dash
    def player_dash(self):
        if self.dash:
            self.move(40)
            dash_sound = pygame.mixer.Sound("../sound/dash.ogg")
            dash_sound.set_volume(0.1)
            dash_sound.play()

    # manage ememy_player_collision
    def ememy_player_collision(self):
        for sprite in self.killable_sprites:
            if pygame.sprite.collide_rect(self, sprite):
                self.damage_taken(sprite.damage)
        for sprite in self.damage_player_object:
            if pygame.sprite.collide_rect(self, sprite):
                self.damage_taken(sprite.damage)

    # reduce dealth when damage taken
    def damage_taken(self, damage):
        if not self.invinsible:
            self.health -= damage
            self.invinsible = True
            hurt_sound = pygame.mixer.Sound("../sound/hurt.ogg")
            hurt_sound.set_volume(0.1)
            hurt_sound.play()
            self.invinsible_time = pygame.time.get_ticks()
        if self.health <= 0:
            Player.game_active = False

    # draw gun at the center pos of the player
    # the gun points in the direction of the mmouse cursor
    def draw_gun(self, offsetx, offsety):
        current_position = pygame.math.Vector2((WIDTH / 2, HEIGHT / 2))
        correction_angle = 0

        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - current_position.x, my - current_position.y
        angle = math.degrees(math.atan2(-dy, dx)) - correction_angle
        if angle > -90 and angle < 90:
            self.gun = pygame.image.load(
                "../graphics/wepons/AK47/AK47_right.png"
            ).convert_alpha()
            self.gun = pygame.transform.scale(self.gun, (80, 80))
        else:
            self.gun = pygame.image.load(
                "../graphics/wepons/AK47/AK47_left.png"
            ).convert_alpha()
            self.gun = pygame.transform.scale(self.gun, (80, 80))

        rot_image = pygame.transform.rotate(self.gun, (angle))

        self.display_surface.blit(
            rot_image, (self.rect[0] - offsetx, self.rect[1] - offsety)
        )

    # update everything
    def update(self):
        self.input()
        self.move(self.speed)
        self.timer()
        self.get_player_state()
        self.player_dash()
        self.animate()
        self.ememy_player_collision()

    # timer for all the countdowns
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
