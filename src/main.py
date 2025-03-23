import sys

import pygame as pygame

from src.UI.UI import UI
from src.enemies.bad_goblin import BadGoblin
from src.common_scripts.clouds import Clouds
from src.enemies.enemie_manager import EnemieManager
from src.levels.level_1.level_1 import Level1
from src.player import Player
from src.tilemap.tilemap import TileMap
from utils import *


class Main:
    def __init__(self):
        # initialize pygame, sound mixer and clock
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()

        # set the main display and title
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Magiko")

        self.running = True
        self.level_1 = Level1("level_1", "orange_superhero")

        self.UI = UI(self.level_1)

    def key_pressed(self, keys):
        """
        Handle the key pressed event
        :param keys: pygame key object
        :return:
        """
        self.level_1.key_pressed(keys)

    def key_up(self, key):
        """
        Handle the key up event
        :param key: pygame key object
        """
        self.level_1.key_up(key)

    def key_down(self, key):
        """
        Handle the key down event
        :param key: pygame key object
        """
        self.level_1.key_down(key)

    def mouse_pressed(self, event):
        """
        Handle the mouse pressed event
        :param event: pygame event object
        """
        self.level_1.mouse_pressed(event)

    def event_manager(self):
        """
        Handle the events
        """
        # check all the events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pressed(event)
            elif event.type == pygame.KEYDOWN:
                pass

            if event.type == pygame.MOUSEMOTION:
                self.UI.mouse_move(pygame.mouse.get_pos())

        # get a list of the current pressed keys
        keys = pygame.key.get_pressed()
        self.key_down(keys)
        if keys[pygame.K_SPACE]:
            pass
        if keys[pygame.K_ESCAPE]:
            self.running = False



    def get_level(self):
        return self.level_1

    def run(self):
        """
        Main game loop
        """
        # main game loop if the game is running
        while self.running:
            # handle the events
            self.event_manager()

            # update current scene
            self.level_1.run(self.screen)

            self.UI.draw(self.screen)

            # set fps
            self.clock.tick(FPS)
            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Main().run()
