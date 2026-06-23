from array import array
from pathlib import Path

import moderngl

from src.utils import HEIGHT, WIDTH, surf_to_texture


def load_shader(path: str) -> str:
    shader_path = Path(path)
    if not shader_path.is_absolute():
        shader_path = Path(__file__).resolve().parent / shader_path
    with shader_path.open('r', encoding='utf-8') as f:
        return f.read()


class Shader:
    def __init__(self, ctx, vertex_path: str, fragment_path: str):
        vertex_code = load_shader(vertex_path)
        fragment_code = load_shader(fragment_path)
        self.ctx = ctx

        self.program = self.ctx.program(vertex_shader=vertex_code, fragment_shader=fragment_code)
        self.quad_buffer = self.ctx.buffer(data=array('f', [
            -1.0,  1.0, 0.0, 0.0,
             1.0,  1.0, 1.0, 0.0,
            -1.0, -1.0, 0.0, 1.0,
             1.0, -1.0, 1.0, 1.0,
        ]))
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])
        self.texture = self.ctx.texture((WIDTH, HEIGHT), 4, data=None)
        self.texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.texture.swizzle = 'BGRA'
        if "tex" in self.program:
            self.program["tex"] = 0

    def render(self, surface):
        tex = surf_to_texture(surface, self.texture)
        tex.use(0)
        self.render_object.render(moderngl.TRIANGLE_STRIP)
