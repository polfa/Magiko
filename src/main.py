import sys

import pygame

from src.UI.UI import UI
from src.common_scripts.lights import Lights
from src.levels.level_1.level_1 import Level1
from src.shaders.lightShader import LightShader
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

        self.ctx = moderngl.create_context()
        self.lightShader = LightShader(self.ctx)

        self.running = True
        self.lights = Lights()
        self.level_1 = Level1("level_1", "orange_superhero", self.screen, self)
        self.UI = UI(self.level_1)
        self.max_lights = 8
        self.t = 0

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
            init_time = pygame.time.get_ticks() / 1000.0
            self.event_manager()
            self.t += 1

            if not self.UI.is_game_paused():
                self.level_1.run(self, self.display)
            final_time = pygame.time.get_ticks() / 1000.0
            offset = self.level_1.player.offset
            self.lights.blit_lights(self.display, offset)
            light_positions = self.lights.get_render_positions(offset, self.max_lights)
            light_colors = [(1.0, 1.0, 1.0)] * self.max_lights
            self.UI.draw(self.display)
            # Render shader -> pinta sobre la pantalla OpenGL
            self.lightShader.render(self.display, offset, light_positions, light_colors)
            # Ahora dibuja la UI encima del frame final


            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main = Main()
    main.run()
    main.game_texture.release()
