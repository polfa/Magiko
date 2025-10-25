from src.shaders.shader import Shader


class LightShader(Shader):
    def __init__(self, ctx):
        vertex_path = "../openGL/lightsVertexShader.glsl"
        fragment_path = "../openGL/lightsFragmentShader.glsl"
        super().__init__(ctx, vertex_path, fragment_path)

    def render(self, screen, offset, light_positions, light_colors):
        self.program['light_positions'] = light_positions
        self.program['light_colors'] = light_colors
        super().render(screen, offset)
