import json

import pygame

from src.utils import TILE_SIZE, WIDTH


class TileMap:
    def __init__(self):
        self.tile_map = {}
        self.tiles = {}
        self.collision_tiles = []
        self.collision_tile_map = {}
        self.light_map = []

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

    def add_to_collision_grid(self, name, pos):
        """
        Add a tile to the collision grid
        :param name: name of the tile (key)
        :param pos: position in the grid
        :return:
        """
        self.collision_tile_map[pos] = name

    def add_light_to_grid(self, name, pos):
        """
        Add a light to the grid
        :param name: name of the light
        :param pos: position in the grid
        :return:
        """
        self.light_map.append(((pos[0], pos[1]), name))

    def get_lights_name_pos(self):
        """
        Get the lights in the grid
        :return:
        """
        return self.light_map

    def remove_light_from_grid(self, pos):
        """
        Remove a light from the grid
        :param pos: position in the grid
        :return:
        """
        self.light_map.pop(pos)

    def save_tile_map_to_json(self, name):
        """
        Save the tile map to a json file
        :param name:
        :return:
        """
        with open(f"../saves/maps/{name}.json", 'w') as file:
            save = {}
            save_grid = {}
            for key, value in self.tile_map.items():
                pos_str = f"{key[0]};{key[1]}"
                save_grid[pos_str] = value
            save_collision_grid = {}
            for key, value in self.collision_tile_map.items():
                pos_str = f"{key[0]};{key[1]}"
                save_collision_grid[pos_str] = value
            save["grid"] = save_grid
            save["collision_grid"] = save_collision_grid
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
            for key, value in save["grid"].items():
                pos = key.split(";")
                self.tile_map[(int(pos[0]), int(pos[1]))] = value
            for key, value in save["collision_grid"].items():
                pos = key.split(";")
                self.collision_tile_map[(int(pos[0]), int(pos[1]))] = value

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
            for pos, tile in self.collision_tile_map.items():
                if not (pos[0] + 3) * TILE_SIZE + offset[0] < 0 or (pos[0] - 3) * TILE_SIZE + offset[0] > WIDTH:
                    screen.blit(self.tiles[tile], (pos[0] * TILE_SIZE + offset[0], pos[1] * TILE_SIZE + offset[1]))
            return
        for pos, tile in self.tile_map.items():
            screen.blit(self.tiles[tile], (pos[0] * TILE_SIZE + offset[0], pos[1] * TILE_SIZE + offset[1]))
