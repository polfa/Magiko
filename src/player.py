import pygame.time as time
from enum import Enum

from src.common_scripts.animation import Animation
from src.common_scripts.collision_manager import CollisionManager
from src.common_scripts.jump import Jump
from src.player_utils.player_stats import PlayerStats
from src.tilemap.tilemap import TileMap
from utils import *


class States(Enum):
    IDLE = "idle"
    RUN = "run"
    JUMP = "jump"
    PRIMARY = "primary"
    SECONDARY = "secondary"
    ULTIMATE = "ultimate"
    FALL = "fall"


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"


class Player:
    def __init__(self, name, level):

        """
        Player class constructor
        :param name: the name defines the player skin
        """

        self.name = name
        self.level = level
        self.stats = PlayerStats()
        self.animations = self.load_animations()

        self.state = States.IDLE
        self.hit_timer = time.get_ticks() / pow(10, 3)
        print(f"hit_timer: {self.hit_timer}")
        self.pos = (WIDTH // 2, 833)
        self.initial_pos = (self.pos[0], self.pos[1])
        self.direction = Direction.RIGHT
        self.speed = self.stats.get_speed()
        self.offset = (0, 0)
        self.limits = level.limits
        self.jump = Jump(self, jump_power=self.stats.get_jump_power(), jump_speed=self.stats.get_jump_speed(),
                         gravity=0.9, jump_cooldown=self.stats.get_jump_cooldown())
        self.collision_manager = CollisionManager()
        self.colliding = False

        self.attack_states = [States.PRIMARY, States.SECONDARY, States.ULTIMATE]

    def load_animations(self):
        name = self.name
        # load animations for each state
        return {
            States.IDLE: Animation(f"img/characters/{name}/idle", 0.1),
            States.RUN: Animation(f"img/characters/{name}/run", 0.03),
            States.JUMP: Animation(f"img/characters/{name}/jump", 1),
            States.FALL: Animation(f"img/characters/{name}/fall", 1),

            States.PRIMARY: Animation(self.stats.get_active_primary().get_animation_path(name), 0.015, loop=False)
            if self.stats.get_active_primary() is not None else None,

            States.SECONDARY: Animation(self.stats.get_active_secondary().get_animation_path(name), 0.022, loop=False)
            if self.stats.get_active_secondary() is not None else None,

            States.ULTIMATE: Animation(self.stats.get_active_ultimate().get_animation_path(name), 0.015, loop=False)
            if self.stats.get_active_ultimate() is not None else None,
        }

    def reset(self):
        self.pos = self.initial_pos
        self.offset = (0, 0)
        self.state = States.IDLE
        self.hit_timer = time.get_ticks() / pow(10, 3)
        self.jump.jumping = False
        self.jump.no_jump_time = self.jump.cooldown

    def set_level(self, level):
        self.level = level

    def set_pos(self, pos):
        self.pos = pos
        self.initial_pos = pos

    def change_state(self, state):
        """
        Change the player state
        :param state: object from States class
        """
        # if the state is the same, do nothing
        if self.state == state:
            return
        # update the current animation
        animation = self.animations[state]
        animation.active = True
        # if the animation is not loop, set the current frame to 0
        if not animation.loop:
            animation.current_frame = 0
        # change the state
        self.state = state

    def rect_contact(self, rect) -> bool:
        """
        Check if the player is in contact with a rect
        :param rect: pygame.Rect object
        :return: True if the player is in contact with the rect, False otherwise
        """
        player_rect = self.get_rect()
        return player_rect.colliderect(rect), rect

    def get_rect(self) -> pygame.Rect:
        """
        Check if the player is in contact with a rect
        :param rect: pygame.Rect object
        :return: True if the player is in contact with the rect, False otherwise
        """
        return pygame.Rect(self.pos[0], self.pos[1], TILE_SIZE, TILE_SIZE)

    def is_hitting(self) -> bool:
        """
        Check if the player is hitting
        :return: True if the player is hitting, False otherwise
        """
        return self.state in self.attack_states

    def has_hit_first(self, enemie) -> bool:
        """
        Check if the player has hit an enemie, it has to be on the last stages of his hit animation so the arm is
        extended and the hit is valid, we also check if the player is facing the enemie
        :param enemie: object from BadGoblin class in src/bad_goblin.py
        :return: True if the player has hit the enemie, False otherwise
        """
        primary = self.animations[States.PRIMARY]
        frame_rate = primary.frame_rate
        animation_time = frame_rate * len(primary.frame_list)
        t = (time.get_ticks() / pow(10, 3)) - self.hit_timer
        if animation_time / 1.3 < t and self.state == States.PRIMARY:
            return True
        return False

    def has_hit_strike(self, enemie) -> bool:
        secondary = self.animations[States.SECONDARY]
        frame_rate = secondary.frame_rate
        animation_time = frame_rate * len(secondary.frame_list)
        t = (time.get_ticks() / pow(10, 3)) - self.hit_timer
        if animation_time / 1.01 < t and self.state == States.SECONDARY:
            return True
        return False

    def has_hit_ultimate(self, enemie) -> bool:
        ult = self.animations[States.ULTIMATE]
        frame_rate = ult.frame_rate
        animation_time = frame_rate * len(ult.frame_list)
        t = (time.get_ticks() / pow(10, 3)) - self.hit_timer
        if animation_time / 1.25 < t and self.state == States.ULTIMATE:
            return True
        return False

    def update(self, screen: pygame.Surface, tilemap: TileMap):
        """
        Update the player position, animation and logic
        :param screen: main pygame display
        :param tilemap: object from TileMap class in src/tilemap.py
        :return: None
        """
        if self.jump.is_jumping():
            if self.jump.jump_speed > 0:
                self.change_state(States.JUMP)
            if self.jump.jump_speed < 0:
                self.change_state(States.FALL)

        # if the current animation is not active, change the state to idle
        if not self.animations[self.state].active:
            self.change_state(States.IDLE)

        # check the collision with the tilemap under the player
        bottom_collision = self.collision_manager.check_bottom_collision(self, tilemap)
        if bottom_collision:
            self.colliding = True
            if self.jump.jump_speed < 0 and bottom_collision:
                self.jump.jumping = False
                self.pos = (self.pos[0], round(self.pos[1] / 64) * 64)
        else:
            if not bottom_collision and self.colliding and not self.jump.is_jumping():
                self.colliding = False
                self.jump.jumping = True
                self.jump.jump_speed = -1
        collectable = self.level.remove_collision_collectable(self.get_rect())
        if collectable is not False:
            if collectable.name == "coin":
                self.stats.add_coins(collectable.value)
            if collectable.name == "mana_potion":
                self.stats.add_mana(collectable.value)
            if collectable.name == "health_potion":
                self.stats.add_health(collectable.value)

        # update the offset, jump logic, animation and render the player
        self.offset = (self.offset[0], -(self.pos[1] - self.initial_pos[1]) // 2)
        self.jump.update(self)
        self.animations[self.state].update()
        self.render(screen)

    def move(self, direction):

        # if the direction is not right or left, do nothing
        if direction != Direction.RIGHT and direction != Direction.LEFT:
            return

        # define Direction.LEFT or right with positive or negative values
        if direction == Direction.LEFT:
            if self.limits[Direction.LEFT.value] >= self.pos[0]:
                return
            mult = -1
        else:
            if self.limits[Direction.RIGHT.value] <= self.pos[0]:
                return
            mult = 1

        # if the player is not in hit state, move the player
        if self.state not in self.attack_states or self.jump.is_jumping():
            if not self.jump.is_jumping():
                self.change_state(States.RUN)
            self.pos = (self.pos[0] + self.speed * mult, self.pos[1])
            self.offset = (self.offset[0] - self.speed * mult, self.offset[1])
            self.direction = direction

    def render(self, screen):
        """
        Render the player
        :param screen: main pygame display
        :return:
        """
        if self.state == States.SECONDARY and self.direction == Direction.LEFT:
            screen.blit(self.animations[self.state].get_current_frame(self.direction.value),
                        (self.pos[0] + self.offset[0] - TILE_SIZE, self.pos[1] + self.offset[1] - TILE_SIZE))
            return
        elif self.state == States.SECONDARY:
            screen.blit(self.animations[self.state].get_current_frame(self.direction.value),
                        (self.pos[0] + self.offset[0], self.pos[1] + self.offset[1] - TILE_SIZE))
            return
        elif self.state == States.ULTIMATE and self.direction == Direction.LEFT:
            if self.animations[self.state].current_frame < 15:
                screen.blit(self.animations[self.state].get_current_frame(self.direction.value),
                            (self.pos[0] + self.offset[0] - TILE_SIZE, self.pos[1] + self.offset[1] - TILE_SIZE))
            else:
                screen.blit(self.animations[self.state].get_current_frame(self.direction.value),
                            (self.pos[0] + self.offset[0] - TILE_SIZE * 3, self.pos[1] + self.offset[1] - TILE_SIZE * 3))
            return
        elif self.state == States.ULTIMATE:
            if self.animations[self.state].current_frame < 15:
                screen.blit(self.animations[self.state].get_current_frame(self.direction.value),
                            (self.pos[0] + self.offset[0], self.pos[1] + self.offset[1] - TILE_SIZE))
            else:
                screen.blit(self.animations[self.state].get_current_frame(self.direction.value),
                            (self.pos[0] + self.offset[0], self.pos[1] + self.offset[1] - TILE_SIZE * 3))
            return
        screen.blit(self.animations[self.state].get_current_frame(self.direction.value), (self.pos[0] + self.offset[0], self.pos[1] + self.offset[1]))

    def key_down(self, keys):
        """
        Check the keys pressed and move the player
        :param keys: list of keys pressed
        :return:
        """
        # we define a movement variable to check if the player is moving
        movement = False
        # check the keys pressed and move the player
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (self.hit_timer > 20 or self.state not in self.attack_states):
            self.move(Direction.LEFT)
            movement = True
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (self.hit_timer > 10 or self.state not in self.attack_states):
            self.move(Direction.RIGHT)
            movement = True

        # if pressing space and the player is not jumping and the jump cooldown is over, jump
        if keys[pygame.K_SPACE]:
            self.jump.start_jump(self)

        # if not moving and not jumping and not hit, change state to idle
        if not movement and not self.jump.is_jumping() and self.state not in self.attack_states:
            self.change_state(States.IDLE)

    def mouse_pressed(self, event):
        """
        Check if the player pressed the mouse button
        :param event: pygame event
        :return:
        """
        # if the player pressed the left mouse button, reset the hit timer and change state to hit
        if self.state != States.PRIMARY and self.state != States.SECONDARY:
            if event.button == 1 and self.stats.get_mana() >= self.stats.get_active_primary().get_mana_cost():
                self.hit_timer = time.get_ticks() / pow(10, 3)
                self.change_state(States.PRIMARY)
                self.stats.add_mana(-self.stats.get_active_primary().get_mana_cost())

            if event.button == 3 and self.stats.get_mana() >= self.stats.get_active_secondary().get_mana_cost():
                self.hit_timer = time.get_ticks() / pow(10, 3)
                self.change_state(States.SECONDARY)
                self.stats.add_mana(-self.stats.get_active_secondary().get_mana_cost())

    def key_pressed(self, event):
        ult_mana_cost = self.stats.get_active_ultimate().get_mana_cost()
        if event.key == pygame.K_q and self.stats.get_mana() >= ult_mana_cost:
            self.hit_timer = time.get_ticks() / pow(10, 3)
            self.change_state(States.ULTIMATE)
            self.stats.add_mana(-ult_mana_cost)
