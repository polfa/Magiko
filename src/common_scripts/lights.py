import pygame

from src.common_scripts.animation import Animation
from src.utils import BASE_PATH, WIDTH, HEIGHT, TILE_SIZE


class PointLight:
    def __init__(self, name, pos):
        self.light = name
        self.pos = pos
        self.image = None
        self.animation = None
        self.color = (1.0, 0.8, 0.55)
        self.radius = 220.0
        self.strength = 1.0
        self.render_offset = (TILE_SIZE // 2, TILE_SIZE // 2)
        if name == "blue_torch":
            self.image = pygame.image.load(BASE_PATH + "/../img/assets/blue_torch.png").convert()
            self.animation = Animation("img/assets/blue_torch", 0.1, loop=True, scale=1)
            self.image.set_colorkey((0, 0, 0))
            self.color = (0.45, 0.75, 1.0)
            self.radius = 260.0
            self.strength = 1.25
            self.render_offset = (TILE_SIZE // 2 - 10, TILE_SIZE // 2)

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
        self.lights = []
        for light in lights:
            self.add_point_light(light[1], light[0])

    def get_lights(self):
        return self.lights

    def blit_lights(self, screen, offset):
        for light in self.lights:
            light.draw(screen, offset)

    def get_render_data(self, offset, max_lights):
        positions = []
        colors = []
        radii = []
        strengths = []

        for light in self.lights:
            render_x = light.pos[0] + offset[0] + light.render_offset[0]
            render_y = light.pos[1] + offset[1] + light.render_offset[1]
            radius = light.radius

            if render_x + radius < 0 or render_x - radius > WIDTH:
                continue
            if render_y + radius < 0 or render_y - radius > HEIGHT:
                continue

            positions.append((render_x, render_y))
            colors.append(light.color)
            radii.append(radius)
            strengths.append(light.strength)

            if len(positions) >= max_lights:
                break

        return {
            "positions": positions,
            "colors": colors,
            "radii": radii,
            "strengths": strengths,
            "count": len(positions),
        }

    def get_render_positions(self, offset, max_lights):
        render_positions = []
        for i in range(max_lights):
            if i >= len(self.lights):
                render_positions.append((0, 0))
                continue
            light = self.lights[i]
            render_positions.append((
                light.pos[0] + offset[0] + light.render_offset[0],
                light.pos[1] + offset[1] + light.render_offset[1],
            ))
        return render_positions.copy()

    def get_render_colors(self, max_lights):
        colors = []
        for i in range(max_lights):
            if i >= len(self.lights):
                colors.append((0.0, 0.0, 0.0))
            else:
                colors.append(self.lights[i].color)
        return colors

    def get_render_radii(self, max_lights):
        radii = []
        for i in range(max_lights):
            if i >= len(self.lights):
                radii.append(0.0)
            else:
                radii.append(self.lights[i].radius)
        return radii

    def get_render_strengths(self, max_lights):
        strengths = []
        for i in range(max_lights):
            if i >= len(self.lights):
                strengths.append(0.0)
            else:
                strengths.append(self.lights[i].strength)
        return strengths
