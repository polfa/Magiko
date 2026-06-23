import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import moderngl
import pygame

from src.UI.UI import UI
from src.common_scripts.lights import Lights
from src.levels.level_1.level_1 import Level1
from src.shaders.lightShader import LightShader
from src.shaders.uiShader import UIShader
from src.utils import FPS, HEIGHT, WIDTH


class Main:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Magiko")
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK,
            pygame.GL_CONTEXT_PROFILE_CORE,
        )

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT),
            pygame.OPENGL | pygame.DOUBLEBUF,
        )

        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = (moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA)

        self.light_shader = LightShader(self.ctx)
        self.ui_shader = UIShader(self.ctx)

        self.running = True
        self.lights = Lights()
        self.level_1 = Level1("level_1", "orange_superhero", self.screen, self)
        self.UI = UI(self.level_1)
        self.max_lights = LightShader.MAX_LIGHTS

        self.world_surface = pygame.Surface((WIDTH, HEIGHT))
        self.ui_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    def key_pressed(self, keys):
        self.level_1.key_pressed(keys)

    def key_up(self, key):
        self.level_1.key_up(key)

    def key_down(self, key):
        self.level_1.key_down(key)

    def mouse_pressed(self, event):
        if event.button == 1 and self.UI.is_clicked(event.pos):
            return
        self.level_1.mouse_pressed(event)

    def event_manager(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pressed(event)
            elif event.type == pygame.MOUSEMOTION:
                self.UI.mouse_move(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                self.key_pressed(event)

        keys = pygame.key.get_pressed()
        self.key_down(keys)
        if keys[pygame.K_ESCAPE]:
            self.running = False

    def get_level(self):
        return self.level_1

    def set_lights(self, lights):
        self.lights.set_lights(lights)

    def run(self):
        while self.running:
            self.event_manager()

            self.world_surface.fill((0, 0, 0))
            if not self.UI.is_game_paused():
                self.level_1.run(self, self.world_surface)

            offset = self.level_1.player.offset
            self.lights.blit_lights(self.world_surface, offset)
            render_data = self.lights.get_render_data(offset, self.max_lights)

            self.light_shader.render(
                self.world_surface,
                render_data["positions"],
                render_data["colors"],
                radii=render_data["radii"],
                strengths=render_data["strengths"],
                light_count=render_data["count"],
            )

            self.ui_surface.fill((0, 0, 0, 0))
            self.UI.draw(self.ui_surface)

            self.ctx.enable(moderngl.BLEND)
            self.ctx.blend_func = (moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA)
            self.ui_shader.render(self.ui_surface)
            self.ctx.disable(moderngl.BLEND)

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    main = Main()
    main.run()
