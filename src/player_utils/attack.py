from abc import ABC, abstractmethod

import pygame


class Attack(ABC):
    def __init__(self, damage, mana_cost, cooldown, icon, name=""):
        self.name = name
        self.damage = damage
        self.cooldown = cooldown
        self.mana_cost = mana_cost
        self.animation = None
        icon = pygame.transform.scale_by(icon, 2)
        self.icon = icon

    def get_icon_path(self):
        return self.icon

    def get_name(self):
        return self.name

    def get_damage(self):
        return self.damage

    def get_cooldown(self):
        return self.cooldown

    def get_mana_cost(self):
        return self.mana_cost

    def set_name(self, name):
        self.name = name

    def set_damage(self, damage):
        self.damage = damage

    def set_cooldown(self, cooldown):
        self.cooldown = cooldown

    def set_mana_cost(self, mana_cost):
        self.mana_cost = mana_cost

    @abstractmethod
    def get_animation_path(self, player_name):
        pass

    @abstractmethod
    def is_area_attack(self):
        pass
