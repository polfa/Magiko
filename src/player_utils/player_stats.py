from enum import Enum

from src.player_utils.abilities import PlayerAbilities
from src.player_utils.attack import Attack
from src.utils import *

class PlayerStats:
    def __init__(self):
        self.stats = {
            "health": 100,
            "max_health": 100,
            "mana": 20,
            "max_mana": 20,
            "damage": 10,
            "coins": 5,
            "speed": 13,
            "jump_power": 25,
            "jump_speed": 0,
            "jump_cooldown": 6,
        }

        self.abilities = PlayerAbilities(self)

    def get_abilities(self):
        return self.abilities.get_player_abilities()

    def get_primary(self, name) -> Attack:
        return self.abilities.get_primary(name)

    def get_active_primary(self) -> Attack:
        return self.abilities.get_active_primary()

    def get_secondary(self, name) -> Attack:
        return self.abilities.get_secondary(name)

    def get_active_secondary(self) -> Attack:
        return self.abilities.get_active_secondary()

    def get_ultimate(self, name) -> Attack:
        return self.abilities.get_ultimate(name)

    def get_active_ultimate(self) -> Attack:
        return self.abilities.get_active_ultimate()

    def get_max_mana(self):
        return self.stats["max_mana"]

    def set_max_mana(self, value):
        self.stats["max_mana"] = value

    def get_max_health(self):
        return self.stats["max_health"]

    def set_max_health(self, value):
        self.stats["max_health"] = value

    def set_primary(self, name):
        self.abilities.set_active_primary(name)

    def set_secondary(self, name):
        self.abilities.set_active_secondary(name)

    def set_ultimate(self, name):
        self.abilities.set_active_ultimate(name)

    def get_abilities_object(self):
        return self.abilities

    def set_abilities(self, abilities):
        self.abilities = abilities

    def get_stat(self, stat):
        return self.stats[stat]

    def set_stat(self, stat, value):
        self.stats[stat] = value

    def add_stat(self, stat, value):
        self.stats[stat] += value

    def remove_stat(self, stat, value):
        self.stats[stat] -= value

    def get_health(self):
        return self.stats["health"]

    def get_mana(self):
        return self.stats["mana"]

    def get_damage(self):
        return self.stats["damage"]

    def get_coins(self):
        return self.stats["coins"]

    def set_health(self, value):
        self.stats["health"] = value

    def set_mana(self, value):
        self.stats["mana"] = value

    def set_damage(self, value):
        self.stats["damage"] = value

    def set_coins(self, value):
        self.stats["coins"] = value

    def add_health(self, value):
        if value < 0:
            if self.stats["health"] + value < 0:
                self.stats["health"] = 0
                return
            elif (self.stats["health"] + value) > self.stats["max_health"]:
                self.stats["health"] = self.stats["max_health"]
                return

        self.stats["health"] += value

    def add_mana(self, value):
        if value < 0:
            if self.stats["mana"] + value < 0:
                self.stats["mana"] = 0
                return
            elif (self.stats["mana"] + value) > self.stats["max_mana"]:
                self.stats["mana"] = self.stats["max_mana"]
                return

        self.stats["mana"] += value

    def add_damage(self, value):
        self.stats["damage"] += value

    def add_coins(self, value):
        self.stats["coins"] += value

    def get_speed(self):
        return self.stats["speed"]

    def get_jump_power(self):
        return self.stats["jump_power"]

    def get_jump_speed(self):
        return self.stats["jump_speed"]

    def get_jump_cooldown(self):
        return self.stats["jump_cooldown"]

    def set_speed(self, value):
        self.stats["speed"] = value

    def set_jump_power(self, value):
        self.stats["jump_power"] = value

    def set_jump_speed(self, value):
        self.stats["jump_speed"] = value

    def set_jump_cooldown(self, value):
        self.stats["jump_cooldown"] = value





