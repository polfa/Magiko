import random
import pygame


class Cloud:
    def __init__(self, pos, img, speed, depth):
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth

    def update(self):
        self.pos[0] += self.speed

    def render(self, surface, offset=(0.1, 0.1)):
        render_pos = (self.pos[0] + offset[0] * self.depth, self.pos[1] + offset[1] * self.depth)
        render_pos = (render_pos[0] % (surface.get_width() + self.img.get_width()) - self.img.get_width(), render_pos[1] % (surface.get_height() + self.img.get_height()) - self.img.get_height())
        surface.blit(self.img, render_pos)


class Clouds:
    def __init__(self, name, count=16):
        self.clouds = []
        img1 = pygame.image.load(f"../img/clouds/{name}/0.png")
        img1 = pygame.transform.scale_by(img1, 2)
        img1.set_colorkey((0, 0, 0))
        img2 = pygame.image.load(f"../img/clouds/{name}/1.png")
        img2 = pygame.transform.scale_by(img2, 2)
        img2.set_colorkey((0, 0, 0))
        cloud_images = [img1, img2]

        for i in range(count):
            self.clouds = []

            for i in range(count):
                self.clouds.append(Cloud((random.random() * 99999, random.random() * 99999), random.choice(cloud_images), random.random() * 0.05 + 0.05, random.random() * 0.6 + 0.2))

            self.clouds.sort(key=lambda x: x.depth)

    def update(self, surface, offset=(0, 0)):
        for cloud in self.clouds:
            cloud.update()

        self.render(surface, offset=offset)

    def render(self, surface, offset=(0, 0)):
        for cloud in self.clouds:
            cloud.render(surface, offset=offset)
