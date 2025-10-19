import math
import random

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


class XpShard(Collectable):
    def __init__(self, pos, value, player):
        name = "xp_shard"
        image_path = BASE_PATH + "/../img/assets/xp_shard.png"
        self.player = player
        super().__init__(name, pos, value, image_path)
        self.pos = [pos[0], player.pos[1]]
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.random_seed = random.randrange(1, 10)
        self.speed = 2

    def get_rect(self):
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.image.get_width() // 2, self.image.get_height() // 2)
        return self.rect

    def update(self, tilemap):
        # Move towards the player with some smooth randomness and rotate
        player_pos = self.player.pos
        direction = (player_pos[0] - self.pos[0], player_pos[1] - self.pos[1])
        distance = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
        if distance > 5:
            direction = (direction[0] / distance, direction[1] / distance)
            speed = (2 + (1 / distance) * 10) * self.speed
            self.pos = (self.pos[0] + direction[0] * speed, math.sin(pygame.time.get_ticks() / 60) * 2 + self.pos[1] + direction[1] * speed)
        else:
            self.pos = player_pos

