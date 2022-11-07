import pygame

# Button class for buttons in game
class Button:
    def __init__(
        self,
        text,
        width,
        height,
        pos,
        rect_color="white",
        font_color=(0, 0, 0),
        font="../font/ARCADECLASSIC.ttf",
    ):
        self.pressed = False
        self.rectangle = pygame.Rect(pos, (width, height))
        self.rectangle.center = pos
        self.rect_color = rect_color
        font = pygame.font.Font(font, 64)
        self.text = font.render(text, True, font_color)
        self.text_rect = self.text.get_rect(center=self.rectangle.center)
        self.screen = pygame.display.get_surface()

    # draw the button on the screen
    def draw(self, func):
        pygame.draw.rect(self.screen, self.rect_color, self.rectangle, border_radius=12)
        self.screen.blit(self.text, self.text_rect)
        self.check_click(func)

    # check if the button is click
    # if button is clicked then run the passed in funtion
    def check_click(self, func):
        mouse_pos = pygame.mouse.get_pos()
        if self.rectangle.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed == True:
                    self.pressed = False
                    func()
