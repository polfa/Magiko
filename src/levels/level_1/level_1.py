from src.levels.level_1.waves import WavesLevel1
from src.levels.level_base import LevelBase

from src.utils import *

class Level1(LevelBase):

    def __init__(self,  name, character_name, screen):
        limits = {"left": 0, "right": WIDTH + TILE_SIZE * 2}
        super().__init__(name, character_name, limits)
        self.wave = WavesLevel1(self.player.initial_pos[1])
        self.screen = screen

    def key_pressed(self, key):
        super().key_pressed(key)

    def key_up(self, key):
        super().key_up(key)

    def key_down(self, key):
        super().key_down(key)

    def mouse_pressed(self, event):
        super().mouse_pressed(event)

    def run(self, screen):
        super().run(screen)

