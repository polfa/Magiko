import random
from random import Random
from enum import Enum

import pygame

from src.common_scripts.animation import Animation
from src.common_scripts.jump import Jump
from src.enemies.life_bar import LifeBar


class State(Enum):
    """
    State class to define the goblin states
    """
    TRACKING = "tracking"
    HIT = "hit"


class BadGoblin:
    def __init__(self, pos=(0, 0)):
        """
        BadGoblin class constructor
        :param pos: Initial position of the goblin
        """
        self.pos = pos
        self.initial_pos = (pos[0], pos[1])
        self.speed = Random().random() / 4 + 0.80
        print(self.speed)
        self.animations = {State.TRACKING: Animation("img/characters/bad_goblin/tracking", 0.05),
                           State.HIT: Animation("img/characters/bad_goblin/hit", 0.02, False)}
        self.direction = "right"
        self.state = State.TRACKING
        self.alive = True
        self.hit_timer = 0
        self.jump = Jump(self, jump_power=5, gravity=0.2)
        self.stop = False

        self.total_life = 100
        self.life = self.total_life
        self.life_bar = LifeBar(self)
        self.random_direction = random.choice(["left", "right"])

    @staticmethod
    def new(pos):
        """
        Copy the goblin
        :return: new goblin object
        """
        return BadGoblin(pos)

    def update(self, player, screen):
        """
        update the goblin position, animation and logic
        :param player: object from Player class in src/player.py
        :param screen: main pygame display
        """
        # if dead, do nothing
        if not self.alive:
            return

        # if state is hit, add to the hit timer
        if self.state == State.HIT:
            self.hit_timer += 1

        # if any animation is not active, set tracking animation
        if not self.animations[self.state].active:
            self.animations[self.state].end()

        # define player position and offset
        offset = player.offset
        player_pos = player.pos

        limits = player.limits


        # if not hitting, move towards player
        if not self.stop:
            if self.pos[0] < limits["left"] and self.direction == "left":
                self.pos = (self.pos[0] + self.speed, self.pos[1])
                if self.direction != "left":
                    self.jump.start_jump(self)
                self.direction = "right"
            elif self.pos[0] > limits["right"] and self.direction == "right":
                self.pos = (self.pos[0] - self.speed, self.pos[1])
                if self.direction != "right":
                    self.jump.start_jump(self)
                self.direction = "left"
            elif self.direction == "right":
                self.pos = (self.pos[0] + self.speed, self.pos[1])
            elif self.direction == "left":
                self.pos = (self.pos[0] - self.speed, self.pos[1])

        # update and display the current animation
        self.jump.update(self)
        self.animations[self.state].update()
        self.render(screen, offset)

    def check_player_hit(self, player):
        # check if player is hit
        self_rect = pygame.Rect(self.pos[0] + 20, self.pos[1] + 15, 40, 64)
        collision, rect = player.rect_contact(self_rect)
        if collision:
            self.stop = True
            # if player is hits the goblin, set alive to False
            if player.has_hit_first(self):
                self.life -= 30
                self.state = State.TRACKING
                self.hit_timer = 0
                self.animations[State.HIT].end()
                if self.direction == "right":
                    self.pos = (self.pos[0] - 10, self.pos[1])
                if self.direction == "left":
                    self.pos = (self.pos[0] + 10, self.pos[1])
                if self.life <= 0:
                    self.alive = False
                return True, "first"
            elif player.has_hit_strike(self):
                self.life -= 50
                self.state = State.TRACKING
                self.hit_timer = 0
                self.animations[State.HIT].end()
                if self.direction == "right":
                    self.pos = (self.pos[0] - 50, self.pos[1])
                if self.direction == "left":
                    self.pos = (self.pos[0] + 50, self.pos[1])
                if self.life <= 0:
                    self.alive = False
                return True, "strike"

            # if player is not hitting the goblin, set hit state and animation
            if self.animations[self.state] != self.animations[State.HIT]:
                self.state = State.HIT
            elif self.animations[self.state] == self.animations[State.HIT]:
                if self.hit_timer > 70:
                    self.hit_timer = 0
                    player.reset()

        else:
            self.stop = False
            # if player is not hitting the goblin, set tracking state and animation
            if self.state == State.HIT:
                self.hit_timer = 0
                self.animations[self.state].end()  # reset the hit animation
            self.state = State.TRACKING

        return False, None

    def reset(self):
        """
        encapsulate the reset logic
        """
        self.pos = self.initial_pos

    def render(self, screen, offset=(0, 0)):
        """
        render the current animation
        :param screen: pygame main display
        :param offset: player offset
        """
        pos = (self.pos[0] + offset[0], self.pos[1] + offset[1])
        self.life_bar.render(screen, pos)
        screen.blit(self.animations[self.state].get_current_frame(self.direction), pos)

