import pygame, sys
from settings import *
from level import Level
from player import *
from enemy import *

# interaction between the player and the tile (borders) implemented
# movement of player implemented

# main game classa
class Game:
    def __init__(self):
        # Initialize pygame object
        pygame.init()
        self.game_active = True
        # Create display surface
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Smilies")
        # Create clock
        self.clock = pygame.time.Clock()
        self.level = Level()

        # play sound
        background_sound = pygame.mixer.Sound(
            "../sound/Memoraphile - Spooky Dungeon.ogg"
        )
        background_sound.set_volume(0.1)
        background_sound.play(-1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            self.screen.fill("#42393a")
            self.clock.tick(FPS)
            if Player.game_active:
                # if game is active run the game
                self.level.run()
            else:
                self.screen.fill("black")
                self.game_over()
                # display the end screen

    def game_over(self):
        font = pygame.font.SysFont(None, 64, bold=True)
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        score_text = font.render(
            "Score: " + str(Enemy.enemies_killed), True, (255, 255, 255)
        )
        text_rect = score_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        game_over_rect = game_over_text.get_rect(
            center=(WIDTH / 2, HEIGHT / 2 - 60)
        )
        self.screen.blit(score_text, text_rect)
        self.screen.blit(game_over_text, game_over_rect)


if __name__ == "__main__":
    game = Game()
    game.run()
