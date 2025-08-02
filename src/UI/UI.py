import pygame

from src.UI.bar import Bar
from src.UI.button import Button
from src.UI.element_box import ElementBox
from src.UI.shop_window import ShopWindow
from src.utils import TILE_SIZE, BASE_PATH, WIDTH, HEIGHT, ELECTRIC_BLUE, MAROON, BEIGE, DARK_BROWN


class UI:
    def __init__(self, level):
        self.level = level
        self.stats = level.player.stats
        scale = (WIDTH / 1920, HEIGHT / 1080)
        self.attack_box = ElementBox(level, path="/../img/UI/attacks/box", x=9 * scale[0], y=0.60 * scale[0], resize_by=2*scale[0], element_number=5)
        self.attack_box.set_element_image(0, lambda:self.stats.get_active_primary().icon)
        self.attack_box.set_element_image(1, lambda:self.stats.get_active_secondary().icon)
        self.attack_box.set_element_image(2, lambda:self.stats.get_active_ultimate().icon)
        self.mana_bar = Bar(TILE_SIZE * 23 * scale[0], TILE_SIZE * 1 * scale[1], TILE_SIZE * 6 * scale[0], TILE_SIZE // 3 * scale[1], ELECTRIC_BLUE, MAROON)
        self.health_bar = Bar(TILE_SIZE * 23 * scale[0], TILE_SIZE * 0.5 * scale[1], TILE_SIZE * 6 * scale[0], (TILE_SIZE // 3) * scale[1], MAROON, ELECTRIC_BLUE)
        self.coin_image = pygame.image.load(BASE_PATH + "/../img/assets/coin.png").convert()
        self.coin_image = pygame.transform.scale(self.coin_image, (TILE_SIZE, TILE_SIZE))
        self.button_size = int(30 * scale[0])
        self.shop_button = Button(" ", TILE_SIZE * 0.5 * scale[0], TILE_SIZE * 1.75 * scale[1], self.button_size, DARK_BROWN, lambda: self.open_shop(), text_color=ELECTRIC_BLUE)
        self.shop_window = ShopWindow(self, self.level)
        self.settings_button = Button(" ", TILE_SIZE * 0.5 * scale[0], TILE_SIZE * 0.75 * scale[1], self.button_size, DARK_BROWN, lambda: self.open_settings(), text_color=ELECTRIC_BLUE)
        self.is_shop_open = False
        self.height = (HEIGHT // 5) * scale[0]
        self.top_rect = pygame.surface.Surface((WIDTH, HEIGHT // 5)).convert()
        self.top_rect.set_alpha(245)  # Ajusta la transparencia (0 = totalmente transparente, 255 = opaco)
        self.top_rect.fill(BEIGE)  # Color negro con opacidad
        self.nut_img = pygame.image.load(BASE_PATH + "/../img/assets/blue_nut.png").convert()
        self.nut_img.set_colorkey((0,0,0))
        self.nut_img = pygame.transform.scale_by(self.nut_img, 1.2)
        self.beige_nut_img = pygame.image.load(BASE_PATH + "/../img/assets/beige_nut.png").convert()
        self.beige_nut_img.set_colorkey((0,0,0))
        self.heart_img = pygame.image.load(BASE_PATH + "/../img/assets/mech_heart.png").convert()
        self.heart_img.set_colorkey((0,0,0))
        self.shop_cart_img = pygame.image.load(BASE_PATH + "/../img/assets/shop_cart.png").convert()
        self.shop_cart_img.set_colorkey((0, 0, 0))
        self.nut_resized = pygame.transform.scale(self.beige_nut_img, (TILE_SIZE, TILE_SIZE))
        self.border_rect = pygame.Rect(0, 0, self.top_rect.get_width(), self.top_rect.get_height())

    def open_settings(self):
        pass

    def open_shop(self):
        self.is_shop_open = True

    def close_shop(self):
        self.is_shop_open = False

    def draw_shop(self, screen):
        self.shop_window.draw(screen)

    def is_game_paused(self):
        if self.is_shop_open:
            return True
        return False

    def draw(self, screen):
        if self.is_shop_open:
            self.draw_shop(screen)
            return
        screen.blit(self.top_rect, (0, 0))
        pygame.draw.rect(screen, DARK_BROWN, self.border_rect, 10)

        self.attack_box.draw(screen)
        self.mana_bar.draw(screen, self.stats.get_mana(), self.stats.get_max_mana())
        self.health_bar.draw(screen, self.stats.get_health(), self.stats.get_max_health())
        self.shop_button.draw(screen)
        self.settings_button.draw(screen)
        self.draw_assets(screen)

    def draw_assets(self, screen):
        # draw coins
        font = pygame.font.Font(BASE_PATH + "/../fonts/ARCADE_N.TTF", 40)
        t = str(self.stats.get_stat("coins"))
        text = font.render(t, True, DARK_BROWN)
        screen.blit(self.coin_image, (TILE_SIZE * 28, TILE_SIZE * 1.75))
        screen.blit(text, (TILE_SIZE * 28 - font.size(t)[0] - 10, TILE_SIZE * 2))
        screen.blit(self.nut_img, (self.mana_bar.rect.x - TILE_SIZE / 1.8, self.mana_bar.rect.y))
        screen.blit(self.heart_img, (self.health_bar.rect.x - TILE_SIZE / 1.8, self.health_bar.rect.y))
        screen.blit(self.nut_resized, (self.settings_button.rect.x + 10, self.settings_button.rect.y + 5))
        screen.blit(self.shop_cart_img, (self.shop_button.rect.x + 14, self.shop_button.rect.y + 5))

    def mouse_move(self, pos):
        self.attack_box.mouse_move(pos)
        self.shop_button.mouse_move(pos)
        if self.is_shop_open:
            self.shop_window.mouse_move(pos)

    def is_clicked(self, pos):
        is_clicked = False
        is_clicked = self.attack_box.mouse_click(pos)
        if self.is_shop_open:
            is_clicked = self.shop_window.is_clicked(pos) if not is_clicked else True
        else:
            is_clicked = self.shop_button.is_clicked(pos) if not is_clicked else True
        return is_clicked
