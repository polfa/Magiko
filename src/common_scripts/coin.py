import math

import pygame

from src.common_scripts.collision_manager import CollisionManager
from src.utils import BASE_PATH, TILE_SIZE


class Coin:
    def __init__(self, name, pos=(0, 0)):
        self.name = name
        self.image = pygame.image.load(BASE_PATH + "/../img/assets/coin.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.pos = [pos[0], pos[1] + TILE_SIZE]
        self.initial_pos = pos
        self.rect = pygame.Rect(self.pos[0], self.pos[1] - TILE_SIZE, self.image.get_width() // 4, self.image.get_height() // 4)

    def update(self, tilemap):
        self.pos = self.initial_pos[0], math.sin(pygame.time.get_ticks() / 100) * 10 + self.initial_pos[1]

    def draw(self, screen, tilemap, offset):
        self.update(tilemap)
        screen.blit(self.image, (self.pos[0] + offset[0], self.pos[1] + offset[1]))


