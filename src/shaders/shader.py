import pygame
from src.utils import *
from array import array
import moderngl


def load_shader(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def surf_to_texture(surf, tex):
    tex.write(surf.get_view('1'))
    return tex


class Shader:
    def __init__(self, ctx,  vertex_path: str, fragment_path: str):
        vertex_code = load_shader(vertex_path)
        fragment_code = load_shader(fragment_path)
        self.ctx = ctx
        self.quad_buffer = self.ctx.buffer(data=array('f', [
            -1.0, 1.0, 0.0, 0.0,
            1.0, 1.0, 1.0, 0.0,
            -1.0, -1.0, 0.0, 1.0,
            1.0, -1.0, 1.0, 1.0,
        ]))
        self.program = self.ctx.program(vertex_shader=vertex_code, fragment_shader=fragment_code)
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])
        self.game_texture = self.ctx.texture((WIDTH, HEIGHT), 4, data=None)
        self.game_texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.game_texture.swizzle = 'BGRA'

    def render(self, screen, offset):
        self.program['tex'] = 0
        self.program['screen_size'] = (WIDTH, HEIGHT)
        game_tex = surf_to_texture(screen, self.game_texture)
        game_tex.use(0)
        self.render_object.render(mode=moderngl.TRIANGLE_STRIP)
