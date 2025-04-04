import sys

import pygame

from src.UI.UI import UI
from src.common_scripts.lights import Lights
from src.levels.level_1.level_1 import Level1
from utils import *
from array import array
import moderngl

vert_shader = '''
#version 330 core

in vec2 vert;
in vec2 texcoord;
out vec2 uvs;

void main() {
    uvs = texcoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}
'''

frag_shader = '''
#version 330 core

uniform sampler2D tex;
uniform vec2 light_positions[8]; // Tres posiciones de luz
uniform float light_decay[8]; // Tres valores de atenuación

in vec2 uvs;
out vec4 f_color;

void main() {
    // Calcular la distancia desde la posición de cada luz a la posición actual del fragmento
    vec2 screen_size = vec2(800.0, 600.0); // Tamaño de la pantalla 
    vec2 frag_position = uvs * screen_size; // Posición de fragmento en píxeles

    vec4 tex_color = texture(tex, uvs);
    vec4 color = vec4(0.0);
    
    if (uvs.y > 0.20) {

        for (int i = 0; i < 8; i++) {
            if (light_positions[i] != vec2(0.0)) {
                float distance = length(frag_position - light_positions[i]); // Distancia al centro
                float attenuation = 1.0 / ((distance * distance + light_decay[i]) * 0.0001); // Atenuación
                color += tex_color * attenuation; // Sumar el efecto de cada luz
            }
        }
        
    } else {
        color = tex_color;
    }

    f_color = color;
}
'''


class Main:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Magiko")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
        self.display = pygame.Surface((WIDTH, HEIGHT))
        self.ctx = moderngl.create_context()

        self.quad_buffer = self.ctx.buffer(data=array('f', [
            -1.0, 1.0, 0.0, 0.0,
            1.0, 1.0, 1.0, 0.0,
            -1.0, -1.0, 0.0, 1.0,
            1.0, -1.0, 1.0, 1.0,
        ]))

        self.program = self.ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])

        self.running = True
        self.lights = Lights()
        self.level_1 = Level1("level_1", "orange_superhero", self.screen, self)
        self.UI = UI(self.level_1)
        self.max_lights = 8
        self.t = 0

        self.game_texture = self.ctx.texture((WIDTH, HEIGHT), 4, data=None)
        self.game_texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.game_texture.swizzle = 'BGRA'


    def surf_to_texture(self, surf, tex):
        tex.write(surf.get_view('1'))
        return tex

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
            self.UI.draw(self.display)
            light_positions = self.lights.get_render_positions(offset, self.max_lights)
            light_decay = [10000.0] * 8
            game_tex = self.surf_to_texture(self.display, self.game_texture)
            game_tex.use(0)

            self.program['tex'] = 0
            self.program['light_positions'] = light_positions
            self.program['light_decay'] = light_decay

            self.render_object.render(mode=moderngl.TRIANGLE_STRIP)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main = Main()
    main.run()
    main.game_texture.release()
