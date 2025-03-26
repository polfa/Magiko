from src.player_utils.attacks.basic import *


class PlayerAbilities:
    def __init__(self, player):
        self.primaries = {
            "basic_primary": BasicPrimaryAttack(damage=5, mana_cost=1, cooldown=1),
            # "fireball": Fireball(player),
            # "lightning": Lightning(player),
        }

        self.secondaries = {
            "basic_secondary": BasicSecondaryAttack(damage=10, mana_cost=2, cooldown=3),
            # "fireball": Fireball(player),
            # "lightning": Lightning(player),
        }

        self.ultimates = {
            "basic_ultimate": BasicUltimateAttack(damage=20, mana_cost=5, cooldown=10),
            # "lightning": Lightning(player),
        }

        self.abilities = list(self.primaries.keys()) + list(self.secondaries.keys()) + list(self.ultimates.keys())

        self.starter_abilities = {
            "basic_primary": self.get_primary("basic_primary"),
            "basic_secondary": self.get_secondary("basic_secondary"),
        }

        self.common_abilities = {
            "basic_primary": self.get_primary("basic_primary"),
            "basic_secondary": self.get_secondary("basic_secondary"),
        }

        self.rare_abilities = {
            # "fireball": Fireball(player),
            # "lightning": Lightning(player),
        }

        self.epic_abilities = {
            # "fireball": Fireball(player),
            # "lightning": Lightning(player),
        }

        self.legendary_abilities = {
            # "fireball": Fireball(player),
            # "lightning": Lightning(player),
        }

        self.current_player_abilities = {
            "primary": self.get_primary("basic_primary"),
            "secondary": self.get_secondary("basic_secondary"),
            "ultimate": self.get_ultimate("basic_ultimate"),
        }

    def set_player_abilities(self, a):
        self.current_player_abilities = a

    def add_hability(self, name):
        if name not in self.abilities:
            if name in self.primaries:
                self.current_player_abilities["primary"] = self.primaries[name]
            elif name in self.secondaries:
                self.current_player_abilities["secondary"] = self.secondaries[name]
            elif name in self.ultimates:
                self.current_player_abilities["ultimate"] = self.ultimates[name]

    def set_active_primary(self, name):
        if name in self.primaries:
            self.current_player_abilities["primary"] = self.primaries[name]
        else:
            raise Exception("set_active_primary: Primary ability not found")

    def set_active_secondary(self, name):
        if name in self.secondaries:
            self.current_player_abilities["secondary"] = self.secondaries[name]
        else:
            raise Exception("set_active_secondary: Ability not found")

    def set_active_ultimate(self, name):
        if name in self.ultimates:
            self.current_player_abilities["ultimate"] = self.ultimates[name]
        else:
            raise Exception("set_active_ultimate: Ability not found")

    def get_active_primary(self):
        return self.current_player_abilities["primary"]

    def get_active_secondary(self):
        return self.current_player_abilities["secondary"]

    def get_active_ultimate(self):
        return self.current_player_abilities["ultimate"]

    def get_player_abilities(self):
        return self.current_player_abilities

    def get_primary(self, name):
        return self.primaries[name]

    def get_secondary(self, name):
        return self.secondaries[name]

    def get_ultimate(self, name):
        return self.ultimates[name]

    def get_ability(self, name):
        if name in self.primaries:
            return self.get_primary(name)
        elif name in self.secondaries:
            return self.get_secondary(name)
        elif name in self.ultimates:
            return self.get_ultimate(name)
        else:
            return None

    def get_starting_abilities(self):
        return self.starter_abilities

    def get_common_abilities(self):
        return self.common_abilities

    def get_rare_abilities(self):
        return self.rare_abilities

    def get_epic_abilities(self):
        return self.epic_abilities

    def get_legendary_abilities(self):
        return self.legendary_abilities

    def is_common(self, name):
        return name in self.common_abilities

    def is_rare(self, name):
        return name in self.rare_abilities

    def is_epic(self, name):
        return name in self.epic_abilities

    def is_legendary(self, name):
        return name in self.legendary_abilities

    def is_ability(self, name):
        return name in self.abilities
