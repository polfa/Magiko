import pygame

from src.utils import TILE_SIZE, BASE_PATH, WIDTH, HEIGHT


class Book:
    def __init__(self, name, pos, image_path, cover_path):
        self.name = name
        self.pos = [pos[0], pos[1]]
        self.image = pygame.image.load(image_path)
        scale = (WIDTH / 1920, HEIGHT / 1080)
        self.image = pygame.transform.scale(self.image, (128 * scale[0], 128 *scale[1]))
        self.image.set_colorkey((0, 0, 0))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())
        self.book_cover_image = pygame.image.load(BASE_PATH + "/../img/books/covers/flower_mariachi.png").convert()
        self.book_cover_image = pygame.transform.scale(self.book_cover_image, (TILE_SIZE * 2 * scale[0], TILE_SIZE * 2 * scale[1])).convert()
        self.book_cover_image.set_colorkey((0, 0, 0))
        self.cover_offset = (5 * scale[0], -10 * scale[1])
        self.in_mouse = False
        self.in_box = True
        self.box_index = -1

    def get_rect(self):
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())
        return self.rect

    def draw(self, screen, offset=(0, 0)):
        screen.blit(self.image, (self.pos[0] + offset[0], self.pos[1] + offset[1]))
        screen.blit(self.book_cover_image, (self.pos[0] + offset[0] + self.cover_offset[0], self.pos[1] + offset[1] + self.cover_offset[1]))

    def mouse_move(self, pos):
        if self.in_mouse:
            self.pos = (pos[0] - TILE_SIZE , pos[1] - TILE_SIZE)
