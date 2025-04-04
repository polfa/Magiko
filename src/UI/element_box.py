import pygame

from src.UI.InfoPlane import InfoPlane
from src.common_scripts.book import Book
from src.utils import BASE_PATH, TILE_SIZE



class ElementBox:
    def __init__(self, level, path, x, y, resize_by=1, element_number=5):
        self.element_number = element_number
        self.resize_by = resize_by
        self.image = pygame.image.load(BASE_PATH + path + "/0.png").convert()
        self.image = pygame.transform.scale_by(self.image, resize_by).convert()
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, self.image.get_width(), self.image.get_height())
        self.pos = (x * TILE_SIZE, y * TILE_SIZE)
        self.selected_element = -1
        self.element_images = [None] * self.element_number

        self.info_plane = InfoPlane(resize_by, level.player.stats)

        self.shadow_surface = pygame.surface.Surface((TILE_SIZE * resize_by + 10, TILE_SIZE * resize_by + 10)).convert()
        self.shadow_surface.set_alpha(75)
        self.shadow_surface.fill((10, 10, 10))
        self.books = []
        self.init_books()

    def init_books(self):
        self.books = [Book("blue_book", (self.pos[0] + 8, self.pos[1] - 56), BASE_PATH + "/../img/books/blue_book.png", BASE_PATH + "/../img/books/covers/flower_mariachi.png"),
                      Book("red_book", (self.pos[0] + TILE_SIZE * 2 + 9*2, self.pos[1] - 56), BASE_PATH + "/../img/books/red_book.png", BASE_PATH + "/../img/books/covers/flower_mariachi.png"),
                      Book("green_book", (self.pos[0] + TILE_SIZE * 4 + 9*3, self.pos[1] - 56), BASE_PATH + "/../img/books/green_book.png", BASE_PATH + "/../img/books/covers/flower_mariachi.png"),
                      Book("yellow_book", (self.pos[0] + TILE_SIZE * 6 + 9*4, self.pos[1] - 56), BASE_PATH + "/../img/books/yellow_book.png", BASE_PATH + "/../img/books/covers/flower_mariachi.png"),
                      Book("purple_book", (self.pos[0] + TILE_SIZE * 8 + 9*5, self.pos[1] - 56), BASE_PATH + "/../img/books/purple_book.png", BASE_PATH + "/../img/books/covers/flower_mariachi.png")]
        for index in range(len(self.books)):
            self.books[index].box_index = index

    def set_element_image(self, index, image_function):
        pass

    def calculate_plane_pos(self):
        return (self.pos[0] - (TILE_SIZE * self.resize_by) // 2 + (TILE_SIZE * self.resize_by) * self.selected_element,
                self.pos[1] + self.info_plane.image.get_height())

    def draw(self, screen):
        screen.blit(self.image, self.pos)

        for i in range(len(self.element_images)):
            if self.element_images[i] is not None:
                image = self.element_images[i]
                if callable(image):
                    image = image()
                else:
                    return
                screen.blit(image,
                            (self.pos[0] + i * self.image.get_width() // self.element_number + 5, self.pos[1] + 5))
        for book in self.books:
            book.draw(screen)

    def mouse_click(self, pos):
        ret = False
        for book in self.books:
            book_collide = book.get_rect().collidepoint(pos)
            collide = self.rect.collidepoint(pos)
            if book.in_mouse and collide:
                for i in range(self.element_number):
                    if self.pos[0] + i * self.image.get_width() // self.element_number < pos[0] < self.pos[0] + (i + 1) * self.image.get_width() // self.element_number:
                        book.in_mouse = False
                        book.in_box = True
                        book.box_index = i
                        book.pos = (self.pos[0] + i * self.image.get_width() // self.element_number, self.pos[1] + 6)
                        ret = True
                        break
            elif book.in_mouse and not collide and book.in_box:
                book.pos = (self.pos[0] + book.box_index * self.image.get_width() // self.element_number, self.pos[1] + 6)
                book.in_mouse = False
                ret = True
            elif not book.in_mouse and book_collide:
                book.in_mouse = True
                ret = True
        return ret

    def mouse_move(self, pos):
        for book in self.books:
            book.mouse_move(pos)

        if self.rect.collidepoint(pos):
            for i in range(self.element_number):
                if self.pos[0] + i * self.image.get_width() // self.element_number < pos[0] < self.pos[0] + (i + 1) * self.image.get_width() // self.element_number:
                    self.selected_element = i
                    break
        else:
            self.selected_element = -1
