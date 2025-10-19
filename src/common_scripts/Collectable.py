import math

import pygame

from src.utils import TILE_SIZE


class Collectable:
    def __init__(self, name, pos, value, image_path):
        self.name = name
        self.pos = [pos[0], pos[1] + TILE_SIZE]
        self.initial_pos = pos
        self.value = value
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.image.set_colorkey((0, 0, 0))
        self.rect = pygame.Rect(self.pos[0], self.pos[1] - TILE_SIZE, self.image.get_width() // 4, self.image.get_height() // 4)

    def get_value(self):
        return self.value

    def get_name(self):
        return self.name

    def get_rect(self):
        return self.rect

    def get_pos(self):
        return self.pos

    def rotate(self, angle):
        """Rotate the collectable image by the given angle."""
        self.image = pygame.transform.rotate(self.image, angle)

    def update(self, tilemap):
        self.pos = self.initial_pos[0], math.sin(pygame.time.get_ticks() / 100) * 10 + self.initial_pos[1]

    def draw(self, screen, tilemap, offset):
        self.update(tilemap)
        screen.blit(self.image, (self.pos[0] + offset[0], self.pos[1] + offset[1]))


