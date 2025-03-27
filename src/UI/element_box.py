import pygame

from src.UI.InfoPlane import InfoPlane
from src.utils import BASE_PATH, TILE_SIZE


class ElementBox:
    def __init__(self, level, path, x, y, resize_by=1, element_number=3):
        self.element_number = element_number
        self.resize_by = resize_by
        self.image = pygame.image.load(BASE_PATH + path + "/0.png").convert()
        self.image = pygame.transform.scale_by(self.image, resize_by).convert()
        self.element_selected_images = [pygame.image.load(BASE_PATH + path + f"/{i}.png") for i in
                                        range(1, element_number + 1)]
        self.element_selected_images = [pygame.transform.scale_by(img, resize_by).convert() for img in
                                        self.element_selected_images]
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, self.image.get_width(), self.image.get_height())
        self.pos = (x * TILE_SIZE, y * TILE_SIZE)
        self.selected_element = -1
        self.element_images = [None] * self.element_number

        self.info_plane = InfoPlane(resize_by, level.player.stats)

    def set_element_image(self, index, image_function):
        self.element_images[index] = image_function

    def calculate_plane_pos(self):
        return (self.pos[0] - (TILE_SIZE * self.resize_by) // 2 + (TILE_SIZE * self.resize_by) * self.selected_element,
                self.pos[1] + self.info_plane.image.get_height())

    def draw(self, screen):
        if self.selected_element == -1:
            screen.blit(self.image, self.pos)
        elif 0 <= self.selected_element < len(self.element_selected_images):
            screen.blit(self.element_selected_images[self.selected_element], self.pos)
            self.info_plane.draw(screen, *self.calculate_plane_pos(), self.selected_element)

        for i in range(len(self.element_images)):
            if self.element_images[i] is not None:
                image = self.element_images[i]
                if callable(image):
                    image = image()
                else:
                    return
                screen.blit(image,
                            (self.pos[0] + i * self.image.get_width() // self.element_number, self.pos[1]))

    def mouse_move(self, pos):
        if self.rect.collidepoint(pos):
            if pos[0] < self.rect.x + self.rect.width // self.element_number:
                self.selected_element = 0
            elif pos[0] < self.rect.x + 2 * self.rect.width // self.element_number:
                self.selected_element = 1
            else:
                self.selected_element = 2
        else:
            self.selected_element = -1