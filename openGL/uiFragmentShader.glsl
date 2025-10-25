#version 330 core

uniform sampler2D tex;
in vec2 v_texcoord;
out vec4 fragColor;

void main() {
    vec4 color = texture(tex, v_texcoord);
    // Mantenemos el canal alpha de la UI
    fragColor = color;
}
