import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from tile import *
from player import *
import random
from enemy import *

# Level class which initializes the player and enemies and the map
class Level:
    def __init__(self, n):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.map_data = load_pygame("../graphics/tilemap/tmx/map_" + str(n) + ".tmx")
        # sptite group setup
        self.obstacle_sprites = pygame.sprite.Group()
        self.killable_sprites = pygame.sprite.Group()
        self.damaging_objects = pygame.sprite.Group()
        self.damage_player_object = pygame.sprite.Group()
        self.visible_sprites = YSortCameraGroup(self.map_data, self.killable_sprites)
        # enemy spawnner

        self.spawn_countdown = INITIAL_SPAWN_TIMER
        self.spawn_enemy = True
        self.spawn_time = 0
        self.enemies_killed = 0
        # create sprite
        self.create_map()
        # play sound
        self.background_sound = pygame.mixer.Sound(
            "../sound/Memoraphile - Spooky Dungeon.ogg"
        )
        self.background_sound.set_volume(0.1)
        self.background_sound.play(-1)
        self.pause = False

    def create_map(self):
        self.spawn_pos = []
        self.enemy_type = list(ENEMIES.keys())
        # create a map blocker
        for x, y, surface in self.map_data.get_layer_by_name("floor_block").tiles():
            x = x * TILESIZE
            y = y * TILESIZE
            Tile((x, y), [self.obstacle_sprites], surface)

        # spawn player in the map
        for x, y, surface in self.map_data.get_layer_by_name("spawnable").tiles():
            x = x * TILESIZE
            y = y * TILESIZE
            self.spawn_pos.append((x, y))
        self.player = Player(
            random.choice(self.spawn_pos),
            [self.visible_sprites],
            self.obstacle_sprites,
            self.visible_sprites,
            self.damaging_objects,
            self.killable_sprites,
            self.damage_player_object,
        )

    def is_paused(self):
        return self.pause

    def pause_game(self, pause):
        self.pause = pause

    # generate random enemies randomly in the map
    def generate_enemies(self, spawn_pos, enemy_type):
        if self.spawn_enemy:
            self.spawn_time = pygame.time.get_ticks()
            Enemy(
                random.choice(spawn_pos),
                random.choice(enemy_type),
                [self.visible_sprites, self.killable_sprites],
                self.obstacle_sprites,
                self.player,
                self.damage_player_object,
                self.visible_sprites,
            )

            self.spawn_enemy = False
            self.spawn_countdown -= SPAWN_DECREMENT_TIME
            if self.spawn_countdown <= MAX_SPAWN_LIMIT:
                self.spawn_countdown = MAX_SPAWN_LIMIT

    def manage_sound(self):
        if not Player.game_active:
            self.background_sound.stop()

    # for all the countdowns
    def timer_countdown(self):
        current_time = pygame.time.get_ticks()
        if (
            current_time - self.spawn_time > self.spawn_countdown
            and len(self.killable_sprites) < MAX_ENEMIES
        ):
            self.spawn_enemy = True

    # update and draw the game
    def run(self):
        if not self.pause:
            self.visible_sprites.custom_draw(self.player)
            self.visible_sprites.update()
            self.timer_countdown()
            if self.player.moved:
                self.generate_enemies(self.spawn_pos, self.enemy_type)
            self.manage_sound()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, map_data, killable_sprites):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.map_data = map_data
        self.killable_sprites = killable_sprites
        self.offset = pygame.math.Vector2()

    # draw on the screen
    def custom_draw(self, player):

        for x, y, surface in self.map_data.get_layer_by_name("base").tiles():
            x = x * TILESIZE
            y = y * TILESIZE
            map_image = pygame.transform.scale(surface, DEFAULT_IMAGE_SIZE)
            map_rect = map_image.get_rect(topleft=(x, y))
            map_offset_pos = map_rect.topleft - self.offset
            self.display_surface.blit(map_image, map_offset_pos)

        # offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        # display health
        black_bar = pygame.Rect(15, 15, 200, 20)
        pygame.draw.rect(self.display_surface, "black", black_bar)
        health_bar = black_bar.copy()
        health_bar.width = player.health / PLAYER_HEALTH * 200
        pygame.draw.rect(self.display_surface, "red", health_bar)

        # display score
        font = pygame.font.SysFont(None, 30, bold=True)
        text = font.render("Score: " + str(Enemy.enemies_killed), True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH / 2, 30))
        self.display_surface.blit(text, text_rect)

        for sprite in self.killable_sprites:
            sprite.draw_health_bar(self.offset.x, self.offset.y)

        player.draw_gun(self.offset.x, self.offset.y)
