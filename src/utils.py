# Description: Archive with the utility methods and constants of the game.
import os
from PIL import Image

import pygame

# ----------------------------------------------------------------
# Util constants

FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (62, 95, 138)
DARK_GRAY = (100, 100, 100)
RED = (255, 100, 100)
GLOWING_CIAN = (0, 190, 190)

ELECTRIC_BLUE = (25, 229, 230)
DARK_BROWN = (28, 13, 2)
MAROON = (92, 10, 10)
BEIGE = (222, 184, 135)
DARK_BEIGE = (139, 115, 85)

# Screen size
WIDTH, HEIGHT = 1920, 1080
SCALE = (WIDTH / 1920, HEIGHT / 1080)

# Tile size
TILE_SIZE = 64

# Player constants
SPEED = 4

COLLISION_TILES = ["blue_bridge"]

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

vert_shader_ui = '''
#version 330 core


in vec2 vert;
in vec2 texcoord;
out vec2 uvs;

void main() {
    uvs = texcoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}
'''

frag_shader_ui = '''
#version 330 core

uniform sampler2D tex;
in vec2 uvs;
out vec4 f_color;

void main() {
    f_color = vec4(texture(tex, uvs).rgb, 1.0);
}
'''

# ----------------------------------------------------------------
# UTILS METHODS


def get_font(font=None):
    # Configurar la fuente
    return pygame.font.Font(font, 50)


def draw_button(screen, rect, text, color):
    font = get_font()
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 2)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_transparent_rect(surface, color, rect, alpha):
    temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    temp_surface.fill((*color, alpha))
    surface.blit(temp_surface, rect.topleft)

def surf_to_texture(surf, tex):
    tex.write(surf.get_view('1'))
    return tex

def load_gif_frames(gif_path):
    gif = Image.open(gif_path)
    frames = []
    for frame in range(gif.n_frames):
        gif.seek(frame)
        frame_image = gif.convert("RGBA")
        frame_data = frame_image.tobytes("raw", "RGBA")
        pygame_image = pygame.image.fromstring(frame_data, frame_image.size, "RGBA")
        frames.append(pygame.transform.scale(pygame_image, (WIDTH, HEIGHT)))
    return frames


def load_images_from_directory(directory):
    images = {}
    # Recorre todos los archivos en el directorio
    for filename in os.listdir(directory):
        # Construye la ruta completa al archivo
        file_path = os.path.join(directory, filename)
        # Comprueba si el archivo es una imagen (por extensión)
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            # Carga la imagen usando Pygame
            image = pygame.image.load(file_path)
            # Añade la imagen al diccionario con el nombre del archivo (sin extensión) como clave
            images[os.path.splitext(filename)[0]] = image
    return images


def round_to_tile(numero):
    # Dividir el número por 40
    division = numero / TILE_SIZE
    # Redondear al entero más cercano
    redondeado = round(division)
    # Multiplicar el resultado redondeado por 40
    resultado = redondeado * TILE_SIZE
    return resultado

