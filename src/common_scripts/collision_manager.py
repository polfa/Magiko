import pygame

from src.tilemap.tilemap import TileMap
from src.utils import TILE_SIZE


class CollisionManager:

    def check_collision(self, entity, tilemap: TileMap) -> bool:
        tilemap_entity_pos = (entity.pos[0] // TILE_SIZE, entity.pos[1] // TILE_SIZE)
        neighbour_tiles = self.get_neighbours(entity, tilemap)
        for pos, name in neighbour_tiles.items():
            if name in tilemap.collision_tiles:
                pos_screen = (int(pos[0]) * TILE_SIZE, int(pos[1]) * TILE_SIZE)
                tile_rect = pygame.Rect(pos_screen, (TILE_SIZE, TILE_SIZE))
                if entity.rect.colliderect(tile_rect):
                    return True
        return False

    def check_bottom_collision(self, entity, tilemap: TileMap) -> bool:
        tilemap_entity_pos = (entity.pos[0] // TILE_SIZE, entity.pos[1] // TILE_SIZE)
        neighbour_tiles = self.get_down_neighbours(entity, tilemap)
        for pos, name in neighbour_tiles.items():
            if name in tilemap.collision_tiles:
                return True
        return False

    @staticmethod
    def get_neighbours(entity, tilemap):
        """
        Get the neighbours of a tile
        :param tilemap: object from TileMap class in src/tilemap.py
        :param entity: object from Player class in src/player.py
        :return: list, list of the neighbours
        """
        tilemap_entity_pos = (entity.pos[0] // TILE_SIZE, entity.pos[1] // TILE_SIZE)
        neighbour_tiles = {}
        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbour_pos = (tilemap_entity_pos[0] + i, tilemap_entity_pos[1] + j)
                neighbour_name = tilemap.collision_tile_map.get(neighbour_pos)
                if neighbour_name:
                    neighbour_tiles[neighbour_pos] = neighbour_name
        return neighbour_tiles

    @staticmethod
    def get_down_neighbours(entity, tilemap):
        """
        Get the neighbours of a tile
        :param tilemap: object from TileMap class in src/tilemap.py
        :param entity: object from Player class in src/player.py
        :return: list, list of the neighbours
        """
        tilemap_entity_pos = (entity.pos[0] // TILE_SIZE, entity.pos[1] // TILE_SIZE)
        neighbour_tiles = {}
        for i in range(0, 2):
            neighbour_pos = (tilemap_entity_pos[0] + i, tilemap_entity_pos[1] + 1)
            neighbour_name = tilemap.collision_tile_map.get(neighbour_pos)
            if neighbour_name:
                neighbour_tiles[neighbour_pos] = neighbour_name
        return neighbour_tiles
