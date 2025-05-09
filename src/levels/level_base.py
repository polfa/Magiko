# This file contains the LevelBase class which is an abstract class that defines the interface for the levels
from abc import ABC, abstractmethod

from src.common_scripts.clouds import Clouds
from src.common_scripts.collectable_definitions import Coin, ManaPotion, HealthPotion
from src.enemies.enemie_manager import EnemieManager
from src.player import Player
from src.tilemap.tilemap import TileMap
from src.utils import *


class LevelBase(ABC):
    @abstractmethod
    def __init__(self, name, character_name, limits, main):
        self.name = name

        # initialize variables
        self.running = True
        self.tilemap = TileMap()
        self.limits = limits
        self.init_tiles(self.tilemap)
        self.tilemap.load_tile_map_from_json(self.name)
        self.wave = None
        self.player = Player(character_name, self)
        self.clouds = Clouds("blue", count=18)
        self.collectables = []

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

    def remove_collision_collectable(self, rect):
        for col in self.collectables:
            if rect.colliderect(col.get_rect()):
                self.collectables.remove(col)
                return col
        return False

    def add_coin(self, pos):
        self.collectables.append(Coin(pos, 1))

    def add_mana_potion(self, pos):
        self.collectables.append(ManaPotion(pos, 10))

    def add_health_potion(self, pos):
        self.collectables.append(HealthPotion(pos, 30))

    def update_collectables(self, screen):
        for col in self.collectables:
            col.draw(screen, self.tilemap, offset=self.player.offset)

    @abstractmethod
    def key_pressed(self, key):
        """
        Handle the key pressed event
        :param key: pygame key object
        :return:
        """
        self.player.key_pressed(key)

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
    def run(self, main, screen):
        """
        Main game loop
        """
        offset = self.player.offset
        # update objects
        screen.fill((0, 0, 0))
        self.clouds.render(screen, offset=offset)
        self.update_collectables(screen)
        self.tilemap.render_tiles(screen, offset, (0, 0))
        self.wave.get_current_wave().update(self.player, screen)
        if self.wave.is_current_wave_over():
            if self.wave.next_wave() is False:
                self.running = False
        self.player.update(screen, self.tilemap)
