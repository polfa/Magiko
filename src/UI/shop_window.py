import pygame

from src.UI.button import Button
from src.utils import WIDTH, HEIGHT, BASE_PATH, DARK_BROWN, BEIGE, MAROON, DARK_BEIGE


class ShopWindow:
    def __init__(self, UI, level):
        self.UI = UI
        self.width = WIDTH // 1.1
        self.height = HEIGHT // 1.1
        self.pos = (WIDTH * 0.05, HEIGHT * 0.05)
        self.window_rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

        self.mana_potion = pygame.image.load(BASE_PATH + "/../img/assets/mana_potion.png")
        self.hability_2 = level.player.level.player.stats.get_active_secondary().icon
        self.hability_3 = level.player.level.player.stats.get_active_ultimate().icon

        self.mana_potion = pygame.transform.scale(self.mana_potion, (self.width // 8, self.width // 8))
        self.hability_2 = pygame.transform.scale(self.hability_2, (self.width // 6, self.width // 6))
        self.hability_3 = pygame.transform.scale(self.hability_3, (self.width // 6, self.width // 6))

        self.hability_size = self.width // 6
        spacing = self.width // 5
        y_position = self.height // 2 - self.hability_size // 2

        self.mana_potion_rect = pygame.Rect(self.pos[0] + spacing, y_position, self.hability_size, self.hability_size)
        self.hability_2_rect = pygame.Rect(self.pos[0] + spacing * 2, y_position, self.hability_size,
                                           self.hability_size)
        self.hability_3_rect = pygame.Rect(self.pos[0] + spacing * 3, y_position, self.hability_size,
                                           self.hability_size)

        self.close_button = Button("Close", self.pos[0] + 50, self.pos[1] + 20, 20, BEIGE,
                                   lambda: self.UI.close_shop())

        self.buy_button_1 = Button("Buy 100G", self.mana_potion_rect.x, self.mana_potion_rect.y + self.hability_size + 10,
                                   30, MAROON, lambda: self.buy_hability(1), text_color=BEIGE)
        self.buy_button_2 = Button("Buy 200G", self.hability_2_rect.x, self.hability_2_rect.y + self.hability_size + 10,
                                   30, MAROON, lambda: self.buy_hability(2), text_color=BEIGE)
        self.buy_button_3 = Button("Buy 300G", self.hability_3_rect.x, self.hability_3_rect.y + self.hability_size + 10,
                                   30, MAROON, lambda: self.buy_hability(3), text_color=BEIGE)

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.fill(BEIGE)  # Fondo con más contraste

        self.title_font = pygame.font.Font(None, 70)
        self.title_surface = self.title_font.render("SHOP", True, BEIGE)
        self.title_rect = self.title_surface.get_rect(center=(self.pos[0] + self.width // 2, self.pos[1] + 50))

        self.slot_surface = pygame.Surface((self.hability_size - 16, self.hability_size - 16), pygame.SRCALPHA)
        self.slot_surface.fill(DARK_BEIGE)


    def draw(self, screen):

        screen.blit(self.surface, (self.window_rect.x, self.window_rect.y))

        pygame.draw.rect(self.surface, DARK_BROWN, self.surface.get_rect(), 10)

        pygame.draw.rect(screen, DARK_BROWN, self.mana_potion_rect, 8)
        screen.blit(self.slot_surface, (self.mana_potion_rect.x + 8, self.mana_potion_rect.y + 8))
        pygame.draw.rect(screen, DARK_BROWN, self.hability_2_rect, 8)
        screen.blit(self.slot_surface, (self.hability_2_rect.x + 8, self.hability_2_rect.y + 8))
        pygame.draw.rect(screen, DARK_BROWN, self.hability_3_rect, 8)
        screen.blit(self.slot_surface, (self.hability_3_rect.x + 8, self.hability_3_rect.y + 8))

        screen.blit(self.mana_potion, self.mana_potion_rect)
        screen.blit(self.hability_2, self.hability_2_rect)
        screen.blit(self.hability_3, self.hability_3_rect)

        pygame.draw.rect(screen, DARK_BROWN, (self.pos[0], self.pos[1], self.width, 80))  # Fondo del título
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
        if self.mana_potion_rect.collidepoint(pos):
            return 1
        elif self.hability_2_rect.collidepoint(pos):
            return 2
        elif self.hability_3_rect.collidepoint(pos):
            return 3
        return 0

    def buy_hability(self, hability_id):
        print(f"Buying hability {hability_id}")