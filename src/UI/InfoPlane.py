import pygame
from src.utils import BASE_PATH, TILE_SIZE
from src.player_utils.player_stats import PlayerStats


class InfoPlane:
    def __init__(self, resize_by, player_stats: PlayerStats):
        self.image = pygame.image.load(BASE_PATH + "/../img/UI/info_plane.png")
        self.image = pygame.transform.scale_by(self.image, resize_by).convert()
        self.image.set_colorkey((0, 0, 0))
        self.font = pygame.font.Font(BASE_PATH + '/../fonts/Pixel_Digivolve.otf', 11)
        self.info_text = [
            lambda : player_stats.get_active_primary().name if player_stats.get_active_primary() is not None else "None",
            lambda : player_stats.get_active_secondary().name if player_stats.get_active_secondary() is not None else "None",
            lambda : player_stats.get_active_ultimate().name if player_stats.get_active_ultimate() is not None else "None"
        ]
        self.damage = [
            lambda: player_stats.get_active_primary().damage if player_stats.get_active_primary() is not None else 0,
            lambda: player_stats.get_active_secondary().damage if player_stats.get_active_secondary() is not None else 0,
            lambda: player_stats.get_active_ultimate().damage if player_stats.get_active_ultimate() is not None else 0
        ]
        self.mana_cost = [
            lambda: player_stats.get_active_primary().get_mana_cost() if player_stats.get_active_primary() is not None else 0,
            lambda: player_stats.get_active_secondary().get_mana_cost() if player_stats.get_active_secondary() is not None else 0,
            lambda: player_stats.get_active_ultimate().get_mana_cost() if player_stats.get_active_ultimate() is not None else 0
        ]
        self.cooldown = [
            lambda: player_stats.get_active_primary().cooldown if player_stats.get_active_primary() is not None else 0,
            lambda: player_stats.get_active_secondary().cooldown if player_stats.get_active_secondary() is not None else 0,
            lambda: player_stats.get_active_ultimate().cooldown if player_stats.get_active_ultimate() is not None else 0
        ]

    def draw(self, screen, x, y, selected_element):
        screen.blit(self.image, (x, y))

        text = self.font.render(self.info_text[selected_element](), True, (255, 255, 255))
        screen.blit(text, (x + 65, y + 30))
        text = self.font.render(f"Damage: {self.damage[selected_element]()}", True, (0, 255, 0))
        screen.blit(text, (x + 75, y + 50))
        text = self.font.render(f"Mana Cost: {self.mana_cost[selected_element]()}", True, (150, 150, 255))
        screen.blit(text, (x + 75, y + 68))
        text = self.font.render(f"Cooldown: {self.cooldown[selected_element]()}", True, (255, 255, 0))
        screen.blit(text, (x + 75, y + 86))
