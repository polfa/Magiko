import json

import pygame

from src.utils import TILE_SIZE, WIDTH


class TileMap:
    def __init__(self):
        self.tile_map = {}
        self.tiles = {}
        self.collision_tiles = []

    def set_collision_tiles(self, tiles):
        """
        Set the collision tiles
        :param tiles: list of tiles
        :return:
        """
        self.collision_tiles = tiles

    def load_tile(self, path, name):
        """
        Load a tile and add it to the tile list
        :param path: path to the tile image
        :param name: name of the tile
        :return: None
        """
        tile = pygame.image.load(f"../img/tiles/{path}").convert()
        tile = pygame.transform.scale_by(tile, 2)
        self.add_to_tile_list(f"{name}", tile)

    def add_to_tile_list(self, name, image):
        """
        Add a tile to the tile list
        :param name: key dor the tile
        :param image:
        :return:
        """
        self.tiles[name] = image

    def add_to_grid(self, name, pos):
        """
        Add a tile to the grid
        :param name: name of the tile (key)
        :param pos: position in the grid
        :return:
        """
        self.tile_map[pos] = name

    def save_tile_map_to_json(self, name):
        """
        Save the tile map to a json file
        :param name:
        :return:
        """
        with open(f"../saves/maps/{name}.json", 'w') as file:
            save = {}
            for key, value in self.tile_map.items():
                pos_str = f"{key[0]};{key[1]}"
                save[pos_str] = value
            json.dump(save, file)
            print("Map saved")

    def load_tile_map_from_json(self, name):
        """
        Load the tile map from a json file
        :param name:
        :return:
        """
        with open(f"../saves/maps/{name}.json", 'r') as file:
            save = json.load(file)
            for key, value in save.items():
                pos = tuple(map(int, key.split(";")))
                self.add_to_grid(value, pos)
            print("Map loaded")

    def render_tiles(self, screen, offset, optimize=True):
        """
        Render the tiles on the screen
        :param screen: pygame display object
        :param offset: camera offset
        :param optimize: boolean to decide if the rendering should be optimized
        :return:
        """
        if optimize:
            for pos, tile in self.tile_map.items():
                if not (pos[0] + 3) * TILE_SIZE + offset[0] < 0 or (pos[0] - 3) * TILE_SIZE + offset[0] > WIDTH:
                    screen.blit(self.tiles[tile], (pos[0] * TILE_SIZE + offset[0], pos[1] * TILE_SIZE + offset[1]))
            return
        for pos, tile in self.tile_map.items():
            screen.blit(self.tiles[tile], (pos[0] * TILE_SIZE + offset[0], pos[1] * TILE_SIZE + offset[1]))
