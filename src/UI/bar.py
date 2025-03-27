import pygame

from src.utils import BASE_PATH


class Bar:
    def __init__(self, x, y, width, height, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(BASE_PATH + '/../fonts/ARCADE_N.ttf', 16)  # Cargar la fuente solo una vez

    def draw(self, screen, current_value, max_value):
        percent = max(0.0, min(current_value / max_value, 1.0))  # Asegurar que esté entre 0 y 1
        filled_rect = pygame.Rect(self.rect.x, self.rect.y, self.width * percent, self.rect.height)

        pygame.draw.rect(screen, self.color, filled_rect)  # Dibujar la barra de progreso
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Dibujar el borde

        # Dibujar texto
        text = f"{current_value}/{max_value}"
        text_render = self.font.render(text, True, self.text_color)
        text_size = text_render.get_size()
        screen.blit(text_render, (self.rect.centerx - text_size[0] // 2, self.rect.centery - text_size[1] // 2))