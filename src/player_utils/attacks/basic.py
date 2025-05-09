from abc import ABC

import pygame

from src.player_utils.attack import Attack
from src.utils import BASE_PATH


class BasicPrimaryAttack(Attack, ABC):
    def __init__(self, damage, mana_cost, cooldown):
        icon = BASE_PATH + "/../img/books/blue_book.png"
        image = pygame.image.load(icon)
        image.set_colorkey((0, 0, 0))
        image.set_colorkey((255, 255, 255))
        area = 1
        super().__init__(damage, mana_cost, cooldown, image, area)
        self.name = "BASIC PRIMARY ATTACK"

    def get_name(self):
        return self.name

    def get_animation_path(self, player_name):
        return f"img/characters/{player_name}/first_hit"

    def is_area_attack(self):
        return False

    def is_multihit(self):
        return False


class BasicSecondaryAttack(Attack, ABC):
    def __init__(self, damage, mana_cost, cooldown):
        icon = BASE_PATH + "/../img/books/blue_book.png"
        image = pygame.image.load(icon)
        image.set_colorkey((0, 0, 0))
        image.set_colorkey((255, 255, 255))
        area = 100
        super().__init__(damage, mana_cost, cooldown, image, area)
        self.name = "BASIC SECONDARY ATTACK"

    def get_name(self):
        return self.name

    def get_animation_path(self, player_name):
        return f"img/characters/{player_name}/strike"

    def is_area_attack(self):
        return False

    def is_multihit(self):
        return True

class BasicUltimateAttack(Attack, ABC):
    def __init__(self, damage, mana_cost, cooldown):
        icon = BASE_PATH + "/../img/books/blue_book.png"
        image = pygame.image.load(icon)
        image.set_colorkey((0, 0, 0))
        image.set_colorkey((255, 255, 255))
        area = 200
        super().__init__(damage, mana_cost, cooldown, image, area)
        self.name = "BASIC ULTIMATE ATTACK"

    def get_name(self):
        return self.name

    def get_animation_path(self, player_name):
        return f"img/characters/{player_name}/basic_ultimate"

    def is_area_attack(self):
        return True

    def is_multihit(self):
        return True

