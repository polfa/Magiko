import pygame

from src.UI.button import Button
from src.utils import WIDTH, HEIGHT


class ShopWindow:
    def __init__(self, UI, level):
        self.UI = UI
        self.width = WIDTH // 1.1
        self.height = HEIGHT // 1.1
        self.pos = (WIDTH * 0.05, HEIGHT * 0.05)
        self.window_rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

        self.hability_1 = level.player.level.player.stats.get_active_primary().icon
        self.hability_2 = level.player.level.player.stats.get_active_secondary().icon
        self.hability_3 = level.player.level.player.stats.get_active_ultimate().icon

        self.hability_1 = pygame.transform.scale(self.hability_1, (self.width // 6, self.width // 6))
        self.hability_2 = pygame.transform.scale(self.hability_2, (self.width // 6, self.width // 6))
        self.hability_3 = pygame.transform.scale(self.hability_3, (self.width // 6, self.width // 6))

        self.hability_size = self.hability_1.get_width()
        spacing = self.width // 5
        y_position = self.height // 2 - self.hability_size // 2

        self.hability_1_rect = pygame.Rect(self.pos[0] + spacing, y_position, self.hability_size, self.hability_size)
        self.hability_2_rect = pygame.Rect(self.pos[0] + spacing * 2, y_position, self.hability_size,
                                           self.hability_size)
        self.hability_3_rect = pygame.Rect(self.pos[0] + spacing * 3, y_position, self.hability_size,
                                           self.hability_size)

        self.close_button = Button("Close", self.pos[0] + 50, self.pos[1] + 20, 20, (200, 50, 50),
                                   lambda: self.UI.close_shop())

        self.buy_button_1 = Button("Buy 100G", self.hability_1_rect.x, self.hability_1_rect.y + self.hability_size + 10,
                                   30, (80, 220, 80), lambda: self.buy_hability(1))
        self.buy_button_2 = Button("Buy 200G", self.hability_2_rect.x, self.hability_2_rect.y + self.hability_size + 10,
                                   30, (80, 220, 80), lambda: self.buy_hability(2))
        self.buy_button_3 = Button("Buy 300G", self.hability_3_rect.x, self.hability_3_rect.y + self.hability_size + 10,
                                   30, (80, 220, 80), lambda: self.buy_hability(3))

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.fill((50, 50, 80, 230))  # Fondo con más contraste

        self.title_font = pygame.font.Font(None, 70)
        self.title_surface = self.title_font.render("SHOP", True, (120, 120, 200))
        self.title_rect = self.title_surface.get_rect(center=(self.pos[0] + self.width // 2, self.pos[1] + 50))

    def draw(self, screen):
        screen.blit(self.surface, (self.window_rect.x, self.window_rect.y))

        pygame.draw.rect(screen, (255, 215, 0), self.hability_1_rect, 3)
        pygame.draw.rect(screen, (255, 215, 0), self.hability_2_rect, 3)
        pygame.draw.rect(screen, (255, 215, 0), self.hability_3_rect, 3)

        screen.blit(self.hability_1, self.hability_1_rect)
        screen.blit(self.hability_2, self.hability_2_rect)
        screen.blit(self.hability_3, self.hability_3_rect)

        pygame.draw.rect(screen, (40, 40, 70, 200), (self.pos[0], self.pos[1], self.width, 80))  # Fondo del título
        screen.blit(self.title_surface, self.title_rect)

        self.close_button.draw(screen)
        self.buy_button_1.draw(screen)
        self.buy_button_2.draw(screen)
        self.buy_button_3.draw(screen)

    def mouse_move(self, pos):
        self.close_button.mouse_move(pos)
        self.buy_button_1.mouse_move(pos)
        self.buy_button_2.mouse_move(pos)
        self.buy_button_3.mouse_move(pos)

    def is_clicked(self, pos):
        if self.close_button.is_clicked(pos):
            return -1
        if self.buy_button_1.is_clicked(pos):
            return 4
        if self.buy_button_2.is_clicked(pos):
            return 5
        if self.buy_button_3.is_clicked(pos):
            return 6
        if self.hability_1_rect.collidepoint(pos):
            return 1
        elif self.hability_2_rect.collidepoint(pos):
            return 2
        elif self.hability_3_rect.collidepoint(pos):
            return 3
        return 0

    def buy_hability(self, hability_id):
        print(f"Buying hability {hability_id}")