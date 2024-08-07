# Description: Archive with the utility methods and constants of the game.
import os
from PIL import Image

import pygame

# ----------------------------------------------------------------
# Util constants

FPS = 144

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (62, 95, 138)
DARK_GRAY = (100, 100, 100)
RED = (255, 100, 100)
GLOWING_CIAN = (0, 190, 190)

# Screen size
WIDTH, HEIGHT = 1920, 1080

# Tile size
TILE_SIZE = 64

# Player constants
SPEED = 4

COLLISION_TILES = ["blue_bridge"]

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

