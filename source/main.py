import pygame, sys
from settings import *
from player import *
from enemy import *
from level import *
from button import *

# interaction between the player and the tile (borders) implemented
# movement of player implemented

# main game class
class Game:
    def __init__(self):
        # Initialize pygame object
        pygame.init()
        self.game_state = "menu"
        self.fill = "black"
        self.level_number = 1
        # Create display surface
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Smilies")
        # Create clock
        self.clock = pygame.time.Clock()
        self.level = None
        self.create_btn()

    # game loop
    def run(self):
        while True:
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            self.clock.tick(FPS)
            if keys[pygame.K_ESCAPE]:
                if self.level != None:
                    self.level.pause_game(True)
                    self.game_state = "paused"
            if self.game_state == "paused":
                self.pause_screen()
            if self.game_state == "menu":
                self.main_menu()
            if self.game_state == "level":
                self.map_selection()
            if self.game_state == "game":
                self.screen.fill(self.fill)
                self.level.run()
                if not Player.game_active:
                    self.game_state = "end"

            if self.game_state == "end":
                self.game_over()

    # creates all the buttons in the game
    def create_btn(self):
        self.start_btn = Button(
            "Start  Game",
            450,
            80,
            (WIDTH / 2, HEIGHT / 2),
        )
        self.over_btn = Button("Play  Again", 450, 80, (WIDTH / 2, 450))
        self.map1_btn = Button("Map 1", 300, 75, (WIDTH / 2, 200))
        self.map2_btn = Button("Map 2", 300, 75, (WIDTH / 2, 300))
        self.map3_btn = Button("Map 3", 300, 75, (WIDTH / 2, 400))
        self.map4_btn = Button("Map 4", 300, 75, (WIDTH / 2, 500))
        self.resume_btn = Button("Resume", 300, 80, (WIDTH / 2, 295))
        self.exit_btn = Button("Exit", 300, 80, (WIDTH / 2, 405))

    # game over screen
    def game_over(self):
        bg = pygame.image.load("../graphics/images/background.png").convert_alpha()
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
        self.screen.blit(bg, (0, 0))
        font = pygame.font.Font("../font/ARCADECLASSIC.ttf", 64)
        game_over_text = font.render("Game  Over", True, (255, 255, 255))
        score_text = font.render(
            "Scored   " + str(Enemy.enemies_killed), True, (255, 255, 255)
        )
        text_rect = score_text.get_rect(center=(WIDTH / 2, 350))
        game_over_rect = game_over_text.get_rect(center=(WIDTH / 2, 275))
        self.screen.blit(score_text, text_rect)
        self.screen.blit(game_over_text, game_over_rect)
        self.over_btn.draw(lambda: self.move_to_next("menu"))

    # pause screen
    def pause_screen(self):
        bg = pygame.image.load("../graphics/images/background.png").convert_alpha()
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
        self.screen.blit(bg, (0, 0))
        self.resume_btn.draw(self.unpause_game)
        self.exit_btn.draw(self.exit_game)

    # unpause the game
    def unpause_game(self):
        if self.level != None:
            self.level.pause_game(False)
            self.game_state = "game"

    # exit the game window
    def exit_game(self):
        pygame.quit()
        sys.exit()

    # main menu screen
    def main_menu(self):
        bg = pygame.image.load("../graphics/images/background.png").convert_alpha()
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
        self.screen.blit(bg, (0, 0))
        self.start_btn.draw(lambda: self.move_to_next("level"))

    # move to the next screen
    def move_to_next(self, state):
        self.game_state = state
        self.reset()

    # map selection screen
    def map_selection(self):
        bg = pygame.image.load("../graphics/images/background.jpg").convert_alpha()
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
        self.screen.blit(bg, (0, 0))
        self.map1_btn.draw(lambda: self.select_map(1, "#42393a"))
        self.map2_btn.draw(lambda: self.select_map(2, "#64adea"))
        self.map3_btn.draw(lambda: self.select_map(3, "#25131a"))
        self.map4_btn.draw(lambda: self.select_map(4, "#191716"))

    # depending on the map selected, get the correct lvl and colors
    def select_map(self, lev_num, bg_color):
        self.level_number = lev_num
        self.fill = bg_color
        self.level = Level(self.level_number)
        self.game_state = "game"

    # reset all the player and enemy states
    def reset(self):
        Player.game_active = True
        Enemy.total_enemies = 0
        Enemy.enemies_killed = 0


if __name__ == "__main__":
    game = Game()
    game.run()
