import random
import pygame


class Cloud:
    __slots__ = ("pos", "img", "speed", "depth")  # Reduce el uso de memoria eliminando __dict__

    def __init__(self, pos, img, speed, depth):
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth

    def update(self):
        self.pos[0] += self.speed

    def render(self, surface, offset=(0.1, 0.1)):
        ox, oy = offset
        w, h = surface.get_size()
        img_w, img_h = self.img.get_size()

        render_x = (self.pos[0] + ox * self.depth) % (w + img_w) - img_w
        render_y = (self.pos[1] + oy * self.depth) % (h + img_h) - img_h

        surface.blit(self.img, (render_x, render_y))


class Clouds:
    def __init__(self, name, count=16):
        # Cargar imágenes solo una vez
        cloud_images = [
            self.load_image(f"../img/clouds/{name}/0.png"),
            self.load_image(f"../img/clouds/{name}/1.png")
        ]

        self.clouds = [
            Cloud(
                (random.uniform(0, 99999), random.uniform(0, 99999)),
                random.choice(cloud_images),
                random.uniform(0.05, 0.1),  # Min: 0.05, Max: 0.1
                random.uniform(0.2, 0.8)   # Min: 0.2, Max: 0.8
            )
            for _ in range(count)
        ]

        self.clouds.sort(key=lambda cloud: cloud.depth)  # Ordenar por profundidad

    @staticmethod
    def load_image(path):
        img = pygame.image.load(path)
        img = pygame.transform.scale_by(img, 2)
        img.set_colorkey((0, 0, 0))
        return img

    def update(self):
        for cloud in self.clouds:
            cloud.update()

    def render(self, surface, offset=(0, 0)):
        for cloud in self.clouds:
            cloud.render(surface, offset=offset)
            cloud.update()
