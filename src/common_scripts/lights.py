import random

import pygame

from src.common_scripts.animation import Animation
from src.utils import BASE_PATH, WIDTH


class PointLight:
    def __init__(self, name, pos):
        self.light = name
        self.pos = pos
        self.image = None
        if name == "blue_torch":
            self.image = pygame.image.load(BASE_PATH + "/../img/assets/blue_torch.png").convert()
            self.animation = Animation("img/assets/blue_torch", 0.1, loop=True, scale=1)
            self.image.set_colorkey((0, 0, 0))

    def draw(self, screen, offset):
        if self.animation is not None:
            self.animation.update()
            screen.blit(self.animation.get_current_frame(), (self.pos[0] + offset[0], self.pos[1] + offset[1]))


class Lights:
    def __init__(self):
        self.lights = []

    def add_point_light(self, name, pos):
        self.lights.append(PointLight(name, pos))

    def set_lights(self, lights):
        for light in lights:
            self.add_point_light(light[1], light[0])

    def get_lights(self):
        return self.lights

    def blit_lights(self, screen, offset):
        for light in self.lights:
            light.draw(screen, offset)

    def get_render_positions(self, offset, max_lights):
        render_positions = []
        scale = WIDTH / 1920
        for i in range(max_lights):
            if i >= len(self.lights):
                render_positions.append((0, 0))
                continue
            light = self.lights[i]
            render_positions.append((light.pos[0] / (2.35 * scale) + offset[0] / (2.4 * scale), light.pos[1] / (1.7 * scale) + offset[1] / (1.7 * scale)))
        return render_positions.copy()
