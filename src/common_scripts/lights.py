import pygame
from src.utils import BASE_PATH


class PointLight:
    def __init__(self, name, pos):
        self.light = name
        self.pos = pos
        self.image = None
        if name == "blue_torch":
            self.image = pygame.image.load(BASE_PATH + "/../img/assets/blue_torch.png").convert()
            self.image.set_colorkey((0, 0, 0))


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
            screen.blit(light.image, (light.pos[0] + offset[0], light.pos[1] + offset[1]))

    def get_render_positions(self, offset, max_lights):
        render_positions = []
        for i in range(max_lights):
            if i >= len(self.lights):
                render_positions.append((0, 0))
                continue
            light = self.lights[i]
            render_positions.append((light.pos[0] / 2.4 + offset[0] / 2.4 , light.pos[1] / 1.7 + offset[1]))
        return render_positions.copy()
