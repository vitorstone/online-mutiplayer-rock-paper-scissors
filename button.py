import pygame
import typing
import colors


class Button:
    def __init__(self, text, x, y, color):
        self.text: pygame.Surface = text
        self.x: int = x
        self.y: int = y
        self.color: typing.Tuple[int, int, int] = color
        self.width: int = 150
        self.height: int = 100

    def draw(self, window: pygame.Surface):

        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font("data/fonts/PressStart2P-Regular.ttf", 15)
        text: pygame.Surface = font.render(self.text, 1, colors.WHITE)
        text_x = self.x + round(self.width / 2) - round(text.get_width() / 2)
        text_y = self.y + round(self.height / 2) - round(text.get_height() / 2)
        window.blit(text, (text_x, text_y))

    def click(self, pos: typing.Tuple[int, int]):
        x1 = pos[0]
        y1 = pos[1]

        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


ALL_BUTTONS = [
    Button("Rock", 50, 500, colors.BLACK),
    Button("Scissors", 250, 500, colors.RED),
    Button("Paper", 450, 500, colors.GREEN),
]
