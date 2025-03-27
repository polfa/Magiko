from src.levels.level_1.waves import WavesLevel1
from src.levels.level_base import LevelBase

from src.utils import *

class Level1(LevelBase):

    def __init__(self,  name, character_name, screen, main):
        limits = {"left": 0, "right": WIDTH + TILE_SIZE * 2}
        super().__init__(name, character_name, limits, main)
        self.wave = WavesLevel1(self.player.initial_pos[1])
        self.screen = screen
        self.tilemap.add_light_to_grid("blue_torch", (300.0, 900.0))
        self.tilemap.add_light_to_grid("blue_torch", (900.0, 900.0))
        self.tilemap.add_light_to_grid("blue_torch", (1500.0, 900.0))
        main.set_lights(self.tilemap.get_lights_name_pos())

    def key_pressed(self, key):
        super().key_pressed(key)

    def key_up(self, key):
        super().key_up(key)

    def key_down(self, key):
        super().key_down(key)

    def mouse_pressed(self, event):
        super().mouse_pressed(event)

    def run(self, main,  screen):
        super().run(main, screen)

