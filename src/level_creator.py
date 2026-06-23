
import moderngl
import pygame

from src.common_scripts.lights import Lights, PointLight
from src.shaders.lightShader import LightShader
from src.shaders.uiShader import UIShader
from src.tilemap.tilemap import TileMap
from src.utils import WIDTH, SPEED, TILE_SIZE, HEIGHT, load_images_from_directory


class LevelCreator:
    def __init__(self):
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK,
            pygame.GL_CONTEXT_PROFILE_CORE,
        )
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption("Magiko")
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = (moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA)
        self.light_shader = LightShader(self.ctx)
        self.ui_shader = UIShader(self.ctx)
        self.name = "level_1"
        self.grid = TileMap()
        self.lights = Lights()
        self.running = True
        self.offset = (0, 0)
        self.floor_pos = TILE_SIZE * 14
        self.max_lights = LightShader.MAX_LIGHTS
        self.init_tiles(self.grid)
        self.placeable_entries = []
        self.placeable_previews = []
        self.mouse_placeable = 0
        self.draw_lines = False
        self.keys_down = {pygame.K_a: False, pygame.K_d: False, pygame.K_w: False, pygame.K_s: False}
        self.grid.load_tile_map_from_json(self.name)
        self.world_surface = pygame.Surface((WIDTH, HEIGHT))
        self.ui_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.mouse_pressed = {"left": False, "right": False, "middle": False}
        self.init_placeables()
        self.sync_lights()

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

    def init_placeables(self):
        self.placeable_entries = [("tile", name) for name in self.grid.tiles.keys()]
        self.placeable_entries.append(("light", "blue_torch"))

        self.placeable_previews = []
        for placeable_type, name in self.placeable_entries:
            if placeable_type == "tile":
                self.placeable_previews.append(self.grid.tiles[name])
                continue

            light = PointLight(name, (0, 0))
            preview = light.image if light.image is not None else pygame.Surface((TILE_SIZE, TILE_SIZE))
            preview.set_colorkey((0, 0, 0))
            self.placeable_previews.append(preview)

    def sync_lights(self):
        self.lights.set_lights(self.grid.get_lights_name_pos())

    def get_selected_placeable(self):
        return self.placeable_entries[self.mouse_placeable]

    def get_mouse_world_pos(self, mouse_pos):
        tile_pos = (
            (mouse_pos[0] - self.offset[0]) // TILE_SIZE,
            (mouse_pos[1] - self.offset[1]) // TILE_SIZE,
        )
        return tile_pos, (float(tile_pos[0] * TILE_SIZE), float(tile_pos[1] * TILE_SIZE))

    def remove_light_at_pos(self, world_pos):
        for index, light in enumerate(self.grid.light_map):
            if light[0] == world_pos:
                self.grid.remove_light_from_grid(index)
                self.sync_lights()
                return True
        return False

    def remove_tile_at_pos(self, tile_pos):
        if tile_pos in self.grid.collision_tile_map:
            del self.grid.collision_tile_map[tile_pos]
            return True
        if tile_pos in self.grid.tile_map:
            del self.grid.tile_map[tile_pos]
            return True
        return False

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
                tile_pos, world_pos = self.get_mouse_world_pos(mouse_pos)
                placeable_type, placeable_name = self.get_selected_placeable()
                if placeable_type == "light":
                    if not any(light_pos == world_pos for light_pos, _ in self.grid.light_map):
                        self.grid.add_light_to_grid(placeable_name, world_pos)
                        self.sync_lights()
                else:
                    is_collision_tile = placeable_name in self.grid.collision_tiles
                    if tile_pos not in self.grid.tile_map and not is_collision_tile:
                        self.grid.add_to_grid(placeable_name, tile_pos)
                    if tile_pos not in self.grid.collision_tile_map and is_collision_tile:
                        self.grid.add_to_collision_grid(placeable_name, tile_pos)
            if self.mouse_pressed["right"]:
                tile_pos, world_pos = self.get_mouse_world_pos(mouse_pos)
                placeable_type, _ = self.get_selected_placeable()
                if placeable_type == "light":
                    self.remove_light_at_pos(world_pos)
                else:
                    self.remove_tile_at_pos(tile_pos)

            self.world_surface.fill((0, 0, 0))
            self.draw_grid_lines(self.world_surface)
            self.grid.render_tiles(self.world_surface, self.offset, optimize=True)
            self.lights.blit_lights(self.world_surface, self.offset)
            render_data = self.lights.get_render_data(self.offset, self.max_lights)
            self.light_shader.render(
                self.world_surface,
                render_data["positions"],
                render_data["colors"],
                radii=render_data["radii"],
                strengths=render_data["strengths"],
                light_count=render_data["count"],
            )

            self.ui_surface.fill((0, 0, 0, 0))
            self.draw_all_tile_types(self.ui_surface)
            self.draw_mouse_image(self.ui_surface)
            self.ui_shader.render(self.ui_surface)
            pygame.display.flip()

    def draw_all_tile_types(self, screen):
        for i in range(0, (WIDTH - 160) // TILE_SIZE):
            if i < len(self.placeable_previews):
                pos = ((i + 1) * TILE_SIZE, TILE_SIZE)
                img = self.placeable_previews[i]
                placeable_type, placeable_name = self.placeable_entries[i]
                if placeable_type == "tile" and "tree" in placeable_name:
                    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                screen.blit(img, pos)
                if i == self.mouse_placeable:
                    pygame.draw.rect(screen, (0, 255, 255), (pos[0], pos[1], TILE_SIZE, TILE_SIZE), 2)
            else:
                break

    def draw_mouse_image(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.mouse_placeable is not None:
            preview = self.placeable_previews[self.mouse_placeable]
            screen.blit(preview, (mouse_pos[0] - TILE_SIZE // 2, mouse_pos[1] - TILE_SIZE // 2))

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
            self.mouse_placeable += 1
            if self.mouse_placeable >= len(self.placeable_previews):
                self.mouse_placeable = 0
        # SCROLL DOWN
        if event.button == 5:
            self.mouse_placeable -= 1
            if self.mouse_placeable < 0:
                self.mouse_placeable = len(self.placeable_previews) - 1


LevelCreator().run()

