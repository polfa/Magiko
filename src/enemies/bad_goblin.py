import random
from random import Random
from enum import Enum

import pygame

from src.common_scripts.animation import Animation
from src.common_scripts.jump import Jump
from src.enemies.life_bar import LifeBar
from src.player import Player
from src.utils import TILE_SIZE


class State(Enum):
    """
    State class to define the goblin states
    """
    TRACKING = "tracking"
    HIT = "hit"


def paint_rect(player, screen, rect, color=(0, 255, 0), offset=True):
    s = rect.copy()
    s.x += player.offset[0]
    s.y += player.offset[1]
    pygame.draw.rect(screen, color, s)


class BadGoblin:
    def __init__(self, pos=(0, 0)):
        """
        BadGoblin class constructor
        :param pos: Initial position of the goblin
        """
        self.damage = 30
        self.pos = pos
        self.initial_pos = (pos[0], pos[1])
        self.speed = Random().random() / 4 + 1.7
        self.attack_animation_speed = 0.02
        self.hit_delay = 36
        self.animations = {State.TRACKING: Animation("img/characters/bad_goblin/tracking", 0.05),
                           State.HIT: Animation("img/characters/bad_goblin/hit", self.attack_animation_speed, False)}
        self.size = TILE_SIZE
        self.direction = 1
        self.state = State.TRACKING
        self.alive = True
        self.hit_timer = 0
        self.attack_damage_applied = False
        self.jump = Jump(self, jump_power=15, gravity=0.9)
        self.stop = False

        self.total_life = 15
        self.life = self.total_life
        self.life_bar = LifeBar(self)
        self.random_direction = random.choice([1, -1])

    @staticmethod
    def new(pos):
        """
        Copy the goblin
        :return: new goblin object
        """
        return BadGoblin(pos)

    def move(self, player):
        limits = player.limits
        if player.pos[0] < self.pos[0]:
            self.direction = -1
        else:
            self.direction = 1

        if random.random() < 0.01:
            self.jump.start_jump()

        self.pos = (self.pos[0] + self.speed * self.direction, self.pos[1])

    def update(self, player, screen):
        """
        update the goblin position, animation and logic
        :param player: object from Player class in src/player.py
        :param screen: main pygame display
        """
        # if dead, do nothing
        if not self.alive:
            return

        self_rect = self.get_self_hit_box()
        collision, rect = player.rect_contact(self_rect)

        if self.state != State.HIT and collision:
            self.start_hit_animation()
        elif self.state == State.HIT:
            if self.hit_timer > self.hit_delay and collision and not self.attack_damage_applied:
                self.attack_damage_applied = True
                player.stats.add_health(-self.damage)
                self.pos = (self.pos[0] - self.size * self.direction, self.pos[1])

        if self.state == State.HIT:
            self.hit_timer += 1

        if self.state == State.HIT and not self.animations[State.HIT].active:
            self.finish_hit_animation()

        if not self.stop:
            self.move(player)

        # update and display the current animation
        self.jump.update(self)
        self.animations[self.state].update()
        self.render(screen, player.offset)

    def check_player_hit(self, player: Player):
        # if dead, do nothing
        if not self.alive:
            return

        # get the active attacks
        active_primary = player.stats.get_active_primary()
        active_secondary = player.stats.get_active_secondary()
        active_ultimate = player.stats.get_active_ultimate()

        self_rect = self.get_player_hit_box(player, active_primary, active_secondary, active_ultimate)
        collision, rect = player.rect_contact(self_rect)

        if collision:
            if self.primary_hit(player, active_primary):
                return active_primary
            elif self.secondary_hit(player, active_secondary):
                return active_secondary
            elif self.ultimate_hit(player, active_ultimate):
                return active_ultimate
        else:
            self.stop = False
            if self.state != State.HIT:
                self.hit_timer = 0
            self.state = State.TRACKING

        return None

    def get_self_hit_box(self, verbose=False):
        if self.direction == 1:
            self_rect = pygame.Rect(self.pos[0] + self.size * 0.8 * self.direction, self.pos[1], self.size / 8, self.size)
        else:
            self_rect = pygame.Rect(self.pos[0], self.pos[1], self.size / 8, self.size)
        return self_rect

    def get_player_hit_box(self, player, active_primary, active_secondary, active_ultimate):
        first = player.state.value == "primary"
        second = player.state.value == "secondary"
        ulti = player.state.value == "ultimate"
        is_multihit = False
        area = 0
        if first and active_primary.is_multihit():
            area = active_primary.get_area() + self.size
            is_multihit = True
        elif second and active_secondary.is_multihit():
            area = active_secondary.get_area() + self.size
            is_multihit = True
        elif ulti and active_ultimate.is_multihit():
            area = active_ultimate.get_area() + self.size
            is_multihit = True
        if is_multihit:
            if self.direction == 1:
                self_rect = pygame.Rect(self.pos[0] - area, self.pos[1] - area, area, area // 1.5)
                self_rect.center = (self.pos[0] + self.size // 2, self.pos[1] + self.size // 2)
            else:
                self_rect = pygame.Rect(self.pos[0], self.pos[1] - area, area + self.size / 10, area // 1.5)
                self_rect.center = (self.pos[0] + self.size // 2, self.pos[1] + self.size // 2)
        else:
            if self.direction == 1:
                self_rect = pygame.Rect(self.pos[0] - self.size * 0.3, self.pos[1], self.size * 1.3, self.size)
            else:
                self_rect = pygame.Rect(self.pos[0], self.pos[1], self.size * 1.3, self.size)
        return self_rect

    def primary_hit(self, player, active_primary):
        if player.has_hit_first(self):
            self.life -= active_primary.damage
            self.state = State.TRACKING
            self.hit_timer = 0
            self.animations[State.HIT].end()
            if player.direction.value == "right":
                self.pos = (self.pos[0] + 10, self.pos[1])
            if player.direction.value == "left":
                self.pos = (self.pos[0] - 10, self.pos[1])
            if self.life <= 0:
                self.alive = False
            return True
        return False

    def secondary_hit(self, player, active_secondary):
        if player.has_hit_strike(self):
            self.life -= active_secondary.damage
            self.state = State.TRACKING
            self.hit_timer = 0
            self.animations[State.HIT].end()
            if player.direction.value == "right":
                self.pos = (self.pos[0] + 50, self.pos[1])
            if player.direction.value == "left":
                self.pos = (self.pos[0] - 50, self.pos[1])
            if self.life <= 0:
                self.alive = False
            return True
        return False

    def ultimate_hit(self, player, active_ultimate):
        if player.has_hit_ultimate(self):
            self.life -= active_ultimate.damage
            self.state = State.TRACKING
            self.hit_timer = 0
            self.animations[State.HIT].end()
            if player.direction.value == "right":
                self.pos = (self.pos[0] + 50, self.pos[1])
            if player.direction.value == "left":
                self.pos = (self.pos[0] - 50, self.pos[1])
            if self.life <= 0:
                self.alive = False
            return True
        return False

    def reset(self):
        """
        encapsulate the reset logic
        """
        self.pos = self.initial_pos

    def start_hit_animation(self):
        self.stop = True
        self.state = State.HIT
        self.hit_timer = 0
        self.attack_damage_applied = False
        self.animations[State.HIT].end()

    def finish_hit_animation(self):
        self.animations[State.HIT].end()
        self.hit_timer = 0
        self.attack_damage_applied = False
        self.stop = False
        self.state = State.TRACKING

    def render(self, screen, offset=(0, 0)):
        """
        render the current animation
        :param screen: pygame main display
        :param offset: player offset
        """
        pos = (self.pos[0] + offset[0], self.pos[1] + offset[1])
        self.life_bar.render(screen, pos)
        screen.blit(self.animations[self.state].get_current_frame(self.direction), pos)

