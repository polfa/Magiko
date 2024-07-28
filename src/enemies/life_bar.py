import pygame.image
from src.utils import TILE_SIZE


class LifeBar:
    def __init__(self, enemy):
        self.enemy = enemy
        self.total = enemy.total_life
        self.bar = {}
        for i in range(0, 101, 5):
            img = pygame.image.load(f"../img/UI/life_bar/{i}.png").convert()
            img.set_colorkey((0, 0, 0))
            img = pygame.transform.scale_by(img, 1.4)
            self.bar[str(i)] = img

    def render(self, screen, pos):
        life = self.enemy.life / self.total * 100
        life_rounded = round(life / 5) * 5
        screen.blit(self.bar[str(life_rounded)], (pos[0] + TILE_SIZE // 6, pos[1] - 20))
