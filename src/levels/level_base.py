# This file contains the LevelBase class which is an abstract class that defines the interface for the levels
from abc import ABC, abstractmethod

from src.common_scripts.clouds import Clouds
from src.enemies.enemie_manager import EnemieManager
from src.player import Player
from src.tilemap.tilemap import TileMap
from src.utils import *


class LevelBase(ABC):
    @abstractmethod
    def __init__(self, name, character_name, limits):
        self.name = name

        # initialize variables
        self.running = True
        self.tilemap = TileMap()
        self.limits = limits
        self.init_tiles(self.tilemap)
        self.tilemap.load_tile_map_from_json(self.name)
        self.wave = None
        self.player = Player(character_name, self)
        self.clouds = Clouds("blue", count=26)

    def init_tiles(self, tilemap):
        """
        Initialize the tilemap with the tiles, the idea is to load the necessary tiles and add them to the grid for
        each level
        :param tilemap: object from TileMap class in src/tilemap.py
        :return:
        """
        tiles = load_images_from_directory(f"../img/tiles/{self.name}")
        collision_tiles = load_images_from_directory(f"../img/tiles/{self.name}/collision")
        tilemap.set_collision_tiles(collision_tiles.keys())
        tiles = {**tiles, **collision_tiles}
        for name, tile in tiles.items():
            tile = tile.convert()
            tile.set_colorkey((0, 0, 0))
            tile = pygame.transform.scale_by(tile, 2)
            if "tree" in name:
                tile = pygame.transform.scale_by(tile, 2)
            tilemap.add_to_tile_list(name, tile)

    @abstractmethod
    def key_pressed(self, key):
        """
        Handle the key pressed event
        :param key: pygame key object
        :return:
        """
        pass

    @abstractmethod
    def key_up(self, key):
        """
        Handle the key up event
        :param key: pygame key object
        """
        pass

    @abstractmethod
    def key_down(self, key):
        """
        Handle the key down event
        :param key: pygame key object
        """
        self.player.key_down(key)

    @abstractmethod
    def mouse_pressed(self, event):
        """
        Handle the mouse pressed event
        :param event: pygame event object
        """
        self.player.mouse_pressed(event)

    @abstractmethod
    def run(self, screen):
        """
        Main game loop
        """

        offset = self.player.offset
        # update objects
        screen.fill((150, 150, 255))
        self.clouds.update(screen, offset=offset)
        self.tilemap.render_tiles(screen, offset, (0, 0))
        self.wave.get_current_wave().update(self.player, screen)
        if self.wave.current_wave_is_empty():
            if self.wave.next_wave() is False:
                self.running = False
        self.player.update(screen, self.tilemap)
