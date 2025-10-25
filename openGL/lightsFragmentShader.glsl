#version 330 core

uniform sampler2D tex;
uniform vec2 light_positions[8];
uniform vec3 light_colors[8]; // puedes añadir color si quieres
uniform vec2 screen_size;
uniform float light_radius;

in vec2 uvs;
out vec4 f_color;

void main() {
    vec2 frag_pos = uvs * screen_size;
    vec4 tex_color = texture(tex, uvs);

    vec3 lighting = vec3(0.2); // luz ambiental
    for (int i = 0; i < 8; i++) {
        vec2 light_pos = light_positions[i];
        if (light_pos == vec2(0.0))
            continue;

        // Distancia al fragmento
        float dist = length(frag_pos - light_pos);

        // Atenuación (ajusta los valores a tu gusto)
        float attenuation = 1.0 / (1.0 + 0.001 * dist + 0.00005 * dist * dist);

        // Difuso radial simple
        float intensity = attenuation * max(0.0, 1.0 - dist / light_radius);

        lighting += light_colors[i] * tex_color.xyz * attenuation;
    }

    f_color = vec4(tex_color.rgb * lighting, tex_color.a);
}
