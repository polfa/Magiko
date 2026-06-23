#version 330 core

uniform sampler2D tex;
uniform vec2  light_positions[100];
uniform vec3  light_colors[100];
uniform float light_radii[100];
uniform float light_strengths[100];
uniform int   light_count;
uniform vec2  screen_size;

in vec2 v_uv;
out vec4 fragColor;

void main() {
    vec2 frag_pos = v_uv * screen_size;
    vec4 texColor = texture(tex, v_uv);
    vec3 lighting = vec3(0.35);

    for (int i = 0; i < light_count; i++) {
        vec2 lp = light_positions[i];
        vec3 lcol = light_colors[i];
        float radius = max(light_radii[i], 1.0);
        float strength = max(light_strengths[i], 0.0);
        float distance_to_light = length(frag_pos - lp);
        float soft = 1.0 - smoothstep(0.6 * radius, radius, distance_to_light);
        float invsq = 1.0 / (1.0 + 0.015 * distance_to_light + 0.00015 * distance_to_light * distance_to_light);
        float attenuation = soft * invsq * strength;

        lighting += lcol * attenuation;
    }

    fragColor = vec4(texColor.rgb * lighting, 1.0);
}
