from src.shaders.shader import Shader
from src.utils import WIDTH, HEIGHT


class LightShader(Shader):
    MAX_LIGHTS = 100

    def __init__(self, ctx):
        vertex_path = "../../openGL/lightsVertexShader.glsl"
        fragment_path = "../../openGL/lightsFragmentShader.glsl"
        super().__init__(ctx, vertex_path, fragment_path)

    def render(self, screen, light_positions, light_colors, radii=None, strengths=None, light_count=None):
        if light_count is None:
            light_count = len(light_positions)
        n = min(self.MAX_LIGHTS, light_count)

        if radii is None:
            radii = [220.0] * n
        if strengths is None:
            strengths = [1.0] * n

        pad_vec2 = [(0.0, 0.0)] * (self.MAX_LIGHTS - n)
        pad_vec3 = [(0.0, 0.0, 0.0)] * (self.MAX_LIGHTS - n)
        pad_flt = [0.0] * (self.MAX_LIGHTS - n)

        self.program["screen_size"] = (WIDTH, HEIGHT)
        self.program["light_count"].value = n
        self.program["light_positions"] = tuple(light_positions[:n] + pad_vec2)
        self.program["light_colors"] = tuple(light_colors[:n] + pad_vec3)
        self.program["light_radii"] = tuple(radii[:n] + pad_flt)
        self.program["light_strengths"] = tuple(strengths[:n] + pad_flt)

        super().render(screen)
