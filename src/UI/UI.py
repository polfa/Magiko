import pygame

from src.UI.bar import Bar
from src.UI.element_box import ElementBox
from src.utils import TILE_SIZE, BASE_PATH


class UI:
    def __init__(self, level):
        self.level = level
        self.attack_box = ElementBox(level, path="/../img/UI/attacks/box", x=12, y=0.25, resize_by=2, element_number=3)
        self.attack_box.set_element_image(0, lambda:level.player.stats.get_active_primary().icon)
        self.attack_box.set_element_image(1, lambda:level.player.stats.get_active_secondary().icon)
        self.attack_box.set_element_image(2, lambda:level.player.stats.get_active_ultimate().icon)
        self.mana_bar = Bar(TILE_SIZE * 23, TILE_SIZE * 1, TILE_SIZE * 6, TILE_SIZE // 3, (30, 100, 255), 15)  # Azul DodgerBlue
        self.health_bar = Bar(TILE_SIZE * 23, TILE_SIZE * 0.5, TILE_SIZE * 6, TILE_SIZE // 3, (178, 34, 34), 100)  # Rojo Firebrick

    def draw(self, screen):
        self.attack_box.draw(screen)
        self.mana_bar.draw(screen, self.level.player.stats.get_stat("mana"))
        self.health_bar.draw(screen, self.level.player.stats.get_stat("health"))

    def mouse_move(self, pos):
        self.attack_box.mouse_move(pos)
