import math

import pygame

from src.common_scripts.Collectable import Collectable
from src.common_scripts.collision_manager import CollisionManager
from src.utils import BASE_PATH, TILE_SIZE


class Coin(Collectable):
    def __init__(self, pos, value):
        name = "coin"
        image_path = BASE_PATH + "/../img/assets/coin.png"
        super().__init__(name, pos, value, image_path)


class HealthPotion(Collectable):
    def __init__(self, pos, value):
        name = "health_potion"
        image_path = BASE_PATH + "/../img/assets/health_potion.png"
        super().__init__(name, pos, value, image_path)


class ManaPotion(Collectable):
    def __init__(self, pos, value):
        name = "mana_potion"
        image_path = BASE_PATH + "/../img/assets/mana_potion.png"
        super().__init__(name, pos, value, image_path)
