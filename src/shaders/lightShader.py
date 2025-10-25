from src.shaders.shader import Shader
from src.utils import WIDTH, HEIGHT


class LightShader(Shader):
    def __init__(self, ctx):
        vertex_path = "../openGL/lightsVertexShader.glsl"
        fragment_path = "../openGL/lightsFragmentShader.glsl"
        super().__init__(ctx, vertex_path, fragment_path)

    def render(self, screen, light_positions, light_colors, radii=None, strengths=None):
        n = min(8, len(light_positions))
        # Rellenos por defecto
        if radii is None:
            radii = [220.0] * n          # radio por defecto (píxeles)
        if strengths is None:
            strengths = [1.0] * n        # intensidad por defecto

        # Completa hasta 8 para los arrays uniform
        pad_vec2 = [(0.0, 0.0)] * (8 - n)
        pad_vec3 = [(0.0, 0.0, 0.0)] * (8 - n)
        pad_flt  = [0.0] * (8 - n)

        self.program['screen_size'] = (WIDTH, HEIGHT)
        self.program['light_count'].value = n

        # ModernGL admite asignar listas/tuplas a arrays de uniforms de vecN/float
        self.program['light_positions'] = tuple(light_positions[:n] + pad_vec2)
        self.program['light_colors']    = tuple(light_colors[:n] + pad_vec3)
        self.program['light_radii']     = tuple(radii[:n] + pad_flt)
        self.program['light_strengths'] = tuple(strengths[:n] + pad_flt)

        super().render(screen)
