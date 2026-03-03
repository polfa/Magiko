from src.shaders.shader import Shader


class UIShader(Shader):
    def __init__(self, ctx):
        vertex_path = "../openGL/uiVertexShader.glsl"
        fragment_path = "../openGL/uiFragmentShader.glsl"
        super().__init__(ctx, vertex_path, fragment_path)

    def render(self, ui_surface, offset=(0, 0)):
        # Simplemente renderiza la textura de UI sin iluminación
        super().render(ui_surface)
