import pygame

from src.utils import BASE_PATH


class Button:
    def __init__(self, text, x, y, size, color, action=None, text_color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = pygame.font.Font(BASE_PATH + "/../fonts/ARCADE_N.TTF", size)
        self.width = self.font.size(text)[0] + 30
        self.height = self.font.size(text)[1] + 20
        self.action = action
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.shadow_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.shadow_surface.set_alpha(100)  # Ajusta la transparencia (0 = totalmente transparente, 255 = opaco)
        self.shadow_surface.fill((0, 0, 0, 100))  # Color negro con opacidad
        self.text_color = text_color

        self.mouse_above = False

    def set_text_color(self, color):
        self.text_color = color

    def set_action(self, action):
        self.action = action

    def do_action(self):
        if self.action:
            self.action()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=(self.x + self.width / 2, self.y + self.height / 1.7))
        if self.mouse_above:
            screen.blit(self.shadow_surface, (self.rect.x, self.rect.y))
        screen.blit(text, text_rect)

    def is_clicked(self, mouse_pos):
        x, y = mouse_pos
        mouse_rect = pygame.Rect(x, y, 1, 1)
        if mouse_rect.colliderect(self.rect):
            self.do_action()
            return True
        return False

    def mouse_move(self, pos):
        x, y = pos
        mouse_rect = pygame.Rect(x, y, 1, 1)
        if mouse_rect.colliderect(self.rect):
            self.mouse_above = True
        else:
            self.mouse_above = False

