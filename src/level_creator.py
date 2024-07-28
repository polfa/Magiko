
import pygame

from src.tilemap.tilemap import TileMap
from src.utils import WIDTH, SPEED, TILE_SIZE, HEIGHT, load_images_from_directory


class LevelCreator:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Magiko")
        self.name = "level_1"
        self.grid = TileMap()
        self.running = True
        self.offset = (0, 0)
        self.floor_pos = TILE_SIZE * 14
        self.init_tiles(self.grid)
        self.tile_types = list(self.grid.tiles.values())
        self.tile_names = list(self.grid.tiles.keys())
        self.mouse_tile = 0
        self.draw_lines = False
        self.keys_down = {pygame.K_a: False, pygame.K_d: False, pygame.K_w: False, pygame.K_s: False}
        self.grid.load_tile_map_from_json(self.name)
        self.mouse_pressed = {"left": False, "right": False, "middle": False}

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

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    self.key_down(event.key)
                if event.type == pygame.KEYUP:
                    self.key_up(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_down(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.mouse_pressed["left"] = False
                    if event.button == 3:
                        self.mouse_pressed["right"] = False
                    if event.button == 2:
                        self.mouse_pressed["middle"] = False

            if self.keys_down[pygame.K_a]:
                self.offset = (self.offset[0] + SPEED, self.offset[1])
            if self.keys_down[pygame.K_d]:
                self.offset = (self.offset[0] - SPEED, self.offset[1])
            if self.keys_down[pygame.K_w]:
                self.offset = (self.offset[0], self.offset[1] + SPEED)
            if self.keys_down[pygame.K_s]:
                self.offset = (self.offset[0], self.offset[1] - SPEED)

            mouse_pos = pygame.mouse.get_pos()
            if self.mouse_pressed["left"]:
                tile_pos = ((mouse_pos[0] - self.offset[0]) // TILE_SIZE, (mouse_pos[1] - self.offset[1]) // TILE_SIZE)
                if tile_pos not in self.grid.tile_map:
                    index = self.mouse_tile
                    self.grid.add_to_grid(self.tile_names[index], tile_pos)
            if self.mouse_pressed["right"]:
                tile_pos = ((mouse_pos[0] - self.offset[0]) // TILE_SIZE, (mouse_pos[1] - self.offset[1]) // TILE_SIZE)
                if tile_pos in self.grid.tile_map:
                    del self.grid.tile_map[tile_pos]

            screen = self.screen
            self.screen.fill((150, 150, 255))
            self.draw_grid_lines(screen)
            self.grid.render_tiles(screen, self.offset, optimize=True)
            self.draw_all_tile_types(screen)
            self.draw_mouse_image(screen)
            pygame.display.flip()

    def draw_all_tile_types(self, screen):
        for i in range(0, (WIDTH - 160) // TILE_SIZE):
            if i < len(self.grid.tiles.values()):
                pos = ((i + 1) * TILE_SIZE, TILE_SIZE)
                img = self.tile_types[i]
                if "tree" in self.tile_names[i]:
                    img = pygame.transform.scale(self.tile_types[i], (TILE_SIZE, TILE_SIZE))
                screen.blit(img, pos)
                if i == self.mouse_tile:
                    pygame.draw.rect(screen, (0, 255, 255), (pos[0], pos[1], TILE_SIZE, TILE_SIZE), 2)
            else:
                break

    def draw_mouse_image(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.mouse_tile is not None:
            screen.blit(self.tile_types[self.mouse_tile], (mouse_pos[0] - TILE_SIZE // 2, mouse_pos[1] - TILE_SIZE // 2))

    def draw_grid_lines(self, screen):
        if not self.draw_lines:
            return
        for i in range(0, WIDTH // TILE_SIZE):
            base_x = i - self.offset[0] // TILE_SIZE
            base_y = i - self.offset[1] // TILE_SIZE
            pygame.draw.line(screen, (120, 120, 120), (base_x * TILE_SIZE + self.offset[0], 0), (base_x * TILE_SIZE + self.offset[0], WIDTH))
            pygame.draw.line(screen, (120, 120, 120), (0, base_y * TILE_SIZE + self.offset[1]), (WIDTH, base_y * TILE_SIZE + self.offset[1]))

    def key_down(self, key):
        if key == pygame.K_a:
            self.keys_down[pygame.K_a] = True
        if key == pygame.K_d:
            self.keys_down[pygame.K_d] = True
        if key == pygame.K_s:
            self.keys_down[pygame.K_s] = True
        if key == pygame.K_w:
            self.keys_down[pygame.K_w] = True

    def key_up(self, key):
        if key == pygame.K_ESCAPE:
            self.running = False
        if key == pygame.K_g:
            self.draw_lines = not self.draw_lines
        if key == pygame.K_o:
            self.grid.save_tile_map_to_json(self.name)
        if key == pygame.K_a:
            self.keys_down[pygame.K_a] = False
        if key == pygame.K_d:
            self.keys_down[pygame.K_d] = False
        if key == pygame.K_s:
            self.keys_down[pygame.K_s] = False
        if key == pygame.K_w:
            self.keys_down[pygame.K_w] = False

    def mouse_down(self, event):
        # LEFT CLICK
        if event.button == 1:
            self.mouse_pressed["left"] = True
        # RIGHT CLICK
        if event.button == 3:
            self.mouse_pressed["right"] = True
        # SCROLL UP
        if event.button == 4:
            self.mouse_tile += 1
            if self.mouse_tile >= len(self.grid.tiles.values()):
                self.mouse_tile = 0
        # SCROLL DOWN
        if event.button == 5:
            self.mouse_tile -= 1
            if self.mouse_tile < 0:
                self.mouse_tile = len(self.grid.tiles.values()) - 1


LevelCreator().run()

