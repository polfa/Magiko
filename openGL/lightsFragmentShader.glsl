#version 330 core

uniform sampler2D tex;
uniform vec2  light_positions[8];
uniform vec3  light_colors[8];
uniform float light_radii[8];      // radio de cada luz en píxeles
uniform float light_strengths[8];  // intensidad (multiplicador) por luz
uniform int   light_count;         // nº de luces válidas
uniform vec2  screen_size;

in vec2 v_uv;
out vec4 fragColor;

void main() {
    vec2 frag_pos = v_uv * screen_size;
    vec4 texColor = texture(tex, v_uv);

    // Luz ambiental base (ajusta si quieres)
    vec3 lighting = vec3(0.35);

    // Acumulamos contribución por luz
    for (int i = 0; i < light_count; i++) {
        vec2  lp   = light_positions[i];
        vec3  lcol = light_colors[i];
        float R    = max(light_radii[i], 1.0);       // evita división por 0
        float S    = max(light_strengths[i], 0.0);   // clamp básico

        float d = length(frag_pos - lp);

        // Perfil de atenuación suave:
        //  - 1.0 en el centro
        //  - 0.0 a partir de R
        //  - borde suave entre ~0.6R y R
        float soft = 1.0 - smoothstep(0.6 * R, R, d);

        // (Opcional) un toque de inverse-square dentro del radio
        float invsq = 1.0 / (1.0 + 0.015 * d + 0.00015 * d * d);

        float att = soft * invsq * S;

        lighting += lcol * att;
    }

    // Forzamos alpha 1.0 en la pasada del mundo (UI se compone después)
    fragColor = vec4(texColor.rgb * lighting, 1.0);
}
