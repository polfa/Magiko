import pygame

from src.utils import BASE_PATH


class Bar:
    def __init__(self, x, y, width, height, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.color = color
        self.text_color = text_color

    def draw(self, screen, current_value, max_value):
        percent = max(0, min(current_value / max_value, 1))  # Asegurar que está entre 0 y 1
        self.rect.width = self.width * percent
        pygame.draw.rect(screen, self.color, self.rect)
        self.rect.width = self.width  # Restaurar tamaño original para el borde
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        # Dibujar texto
        font = pygame.font.Font(BASE_PATH + '/../fonts/ARCADE_N.ttf', 16)
        text = f"{current_value}/{max_value}"
        text_render = font.render(text, True, self.text_color)
        screen.blit(text_render, (self.rect.x + self.rect.width // 2 - font.size(text)[0] // 2,
                                  self.rect.y + self.rect.height // 2 - font.size(text)[1] // 2))
