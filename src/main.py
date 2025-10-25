import sys

import pygame

from src.UI.UI import UI
from src.common_scripts.lights import Lights
from src.levels.level_1.level_1 import Level1
from src.shaders.lightShader import LightShader
from src.shaders.uiShader import UIShader
from utils import *
from array import array
import moderngl


# --- Cargar código GLSL desde archivo ---
def load_shader(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

class Main:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Magiko")
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
        self.display = pygame.Surface((WIDTH, HEIGHT))
        self.ui_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        # --- Contexto OpenGL ModernGL ---
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = (moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA)

        # --- Shaders ---
        self.lightShader = LightShader(self.ctx)
        self.uiShader = UIShader(self.ctx)

        self.running = True
        self.lights = Lights()
        self.level_1 = Level1("level_1", "orange_superhero", self.screen, self)
        self.UI = UI(self.level_1)
        self.max_lights = 8

    def key_pressed(self, keys):
        """
        Handle the key pressed event
        :param keys: pygame key object
        :return:
        """
        self.level_1.key_pressed(keys)

    def key_up(self, key):
        """
        Handle the key up event
        :param key: pygame key object
        """
        self.level_1.key_up(key)

    def key_down(self, key):
        """
        Handle the key down event
        :param key: pygame key object
        """
        self.level_1.key_down(key)

    def mouse_pressed(self, event):
        """
        Handle the mouse pressed event
        :param event: pygame event object
        """
        if event.button == 1:
            if self.UI.is_clicked(event.pos):
                return
        self.level_1.mouse_pressed(event)

    def event_manager(self):
        """
        Handle the events
        """
        # check all the events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pressed(event)
            elif event.type == pygame.KEYDOWN:
                pass

            if event.type == pygame.MOUSEMOTION:
                self.UI.mouse_move(pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN:
                self.key_pressed(event)

        # get a list of the current pressed keys
        keys = pygame.key.get_pressed()
        self.key_down(keys)
        if keys[pygame.K_SPACE]:
            pass
        if keys[pygame.K_ESCAPE]:
            self.running = False

    def get_level(self):
        return self.level_1

    def set_lights(self, lights):
        self.lights.set_lights(lights)


    def run(self):
        while self.running:
            # Antes de self.lightShader.render(...)
            self.ctx.clear(0.0, 0.0, 0.0, 1.0)

            self.event_manager()

            # --- Render juego base ---
            if not self.UI.is_game_paused():
                self.level_1.run(self, self.display)

            offset = self.level_1.player.offset
            self.lights.blit_lights(self.display, offset)
            # ...
            light_positions = self.lights.get_render_positions(offset, self.max_lights)
            light_colors = [(1.0, 1.0, 1.0)] * len(light_positions)

            # Ejemplo: radios distintos por luz (en píxeles)
            radii = [300.0] * len(light_positions)
            # Intensidades (1.0 = normal, 2.0 = más brillante, etc.)
            strengths = [1.2] * len(light_positions)

            self.lightShader.render(self.display, light_positions, light_colors, radii, strengths)
            # ...

            # --- 2) Render UI (encima, con transparencia) ---
            self.ui_surface.fill((0, 0, 0, 0))
            self.UI.draw(self.ui_surface)
            self.uiShader.render(self.ui_surface)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main = Main()
    main.run()
