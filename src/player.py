from enum import Enum

from src.common_scripts.animation import Animation
from src.common_scripts.collision_manager import CollisionManager
from src.common_scripts.jump import Jump
from src.tilemap.tilemap import TileMap
from utils import *


class States(Enum):
    IDLE = "idle"
    RUN = "run"
    JUMP = "jump"
    HIT = "hit"
    STRIKE = "strike"
    FALL = "fall"


class Player:
    def __init__(self, name):

        """
        Player class constructor
        :param name: the name defines the player skin
        """

        self.name = name

        # load animations for each state
        self.animations = {
            States.IDLE: Animation(f"img/characters/{name}/idle", 0.1),
            States.RUN: Animation(f"img/characters/{name}/run", 0.03),
            States.JUMP: Animation(f"img/characters/{name}/jump", 1),
            States.FALL: Animation(f"img/characters/{name}/fall", 1),
            States.HIT: Animation(f"img/characters/{name}/first_hit", 0.03, loop=False),
            States.STRIKE: Animation(f"img/characters/{name}/strike", 0.045, loop=False),
        }
        # set initial attributes
        self.hit_timer = 0
        self.state = States.IDLE
        self.pos = (WIDTH // 2, 833)
        self.initial_pos = (self.pos[0], self.pos[1])
        self.direction = "right"
        self.speed = 4
        self.offset = (0, 0)
        self.limits = {"left": 0, "right": WIDTH + TILE_SIZE * 2}
        self.jump = Jump(self, jump_power=10, jump_speed=0, gravity=0.2, jump_cooldown=15)
        self.collision_manager = CollisionManager()
        self.colliding = False

    def reset(self):
        self.pos = self.initial_pos
        self.offset = (0, 0)
        self.state = States.IDLE
        self.hit_timer = 0
        self.jump.jumping = False
        self.jump.no_jump_time = self.jump.cooldown

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
        return player_rect.colliderect(rect)

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
        return self.state == States.HIT or self.state == States.STRIKE

    def has_hit_first(self, enemie) -> bool:
        """
        Check if the player has hit an enemie, it has to be on the last stages of his hit animation so the arm is
        extended and the hit is valid, we also check if the player is facing the enemie
        :param enemie: object from BadGoblin class in src/bad_goblin.py
        :return: True if the player has hit the enemie, False otherwise
        """
        if 40 < self.hit_timer < 60 and self.state == States.HIT:
            if self.direction == enemie.direction:
                return False
            return True
        return False

    def has_hit_strike(self, enemie) -> bool:
        if 120 < self.hit_timer < 160 and self.state == States.STRIKE:
            if self.direction == enemie.direction:
                return False
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

        # if the player is in hit state, increase the hit timer
        if self.state == States.HIT or self.state == States.STRIKE:
            self.hit_timer += 1

        # if the current animation is not active, change the state to idle
        if not self.animations[self.state].active:
            self.hit_timer = 0
            self.change_state(States.IDLE)

        # check collisions
        collision = self.collision_manager.check_collision(self, tilemap)
        if collision:
            self.colliding = True
            if self.jump.jump_speed < 0:
                self.jump.jumping = False
                self.pos = (self.pos[0], ((self.pos[1] - 1) // 64) * 64)
        else:
            if not self.collision_manager.check_bottom_collision(self, tilemap) and self.colliding and not self.jump.is_jumping():
                self.colliding = False
                self.jump.jumping = True
                self.jump.jump_speed = -1

        # update the offset, jump logic, animation and render the player
        self.offset = (self.offset[0], -(self.pos[1] - self.initial_pos[1]) // 2)
        self.jump.update(self)
        self.animations[self.state].update()
        self.render(screen)

    def move(self, direction):
        """
        Move the player in a direction
        :param direction: String, "right" or "left"
        :return:
        """
        # if the direction is not right or left, do nothing
        if direction != "right" and direction != "left":
            return

        # define left or right with positive or negative values
        if direction == "left":
            if self.limits["left"] >= self.pos[0]:
                return
            mult = -1
        else:
            if self.limits["right"] <= self.pos[0]:
                return
            mult = 1

        # if the player is not in hit state, move the player
        if self.state != States.HIT or self.state != States.STRIKE or self.jump.is_jumping():
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
        if self.state == States.STRIKE and self.direction == "left":
            screen.blit(self.animations[self.state].get_current_frame(self.direction),
                        (self.pos[0] + self.offset[0] - TILE_SIZE, self.pos[1] + self.offset[1] - TILE_SIZE))
            return
        elif self.state == States.STRIKE:
            screen.blit(self.animations[self.state].get_current_frame(self.direction),
                        (self.pos[0] + self.offset[0], self.pos[1] + self.offset[1] - TILE_SIZE))
            return
        screen.blit(self.animations[self.state].get_current_frame(self.direction), (self.pos[0] + self.offset[0], self.pos[1] + self.offset[1]))

    def key_down(self, keys):
        """
        Check the keys pressed and move the player
        :param keys: list of keys pressed
        :return:
        """
        # we define a movement variable to check if the player is moving
        movement = False

        # check the keys pressed and move the player
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (self.hit_timer > 20 or self.state != States.HIT and self.state != States.STRIKE):
            self.move("left")
            movement = True
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (self.hit_timer > 10 or self.state != States.HIT and self.state != States.STRIKE):
            self.move("right")
            movement = True

        # if pressing space and the player is not jumping and the jump cooldown is over, jump
        if keys[pygame.K_SPACE]:
            self.jump.start_jump(self)

        # if not moving and not jumping and not hit, change state to idle
        if not movement and not self.jump.is_jumping() and self.state != States.HIT and self.state != States.STRIKE:
            self.change_state(States.IDLE)

    def mouse_pressed(self, event):
        """
        Check if the player pressed the mouse button
        :param event: pygame event
        :return:
        """
        # if the player pressed the left mouse button, reset the hit timer and change state to hit
        if self.state != States.HIT and self.state != States.STRIKE:
            if event.button == 1:
                self.hit_timer = 0
                self.change_state(States.HIT)
            if event.button == 3:
                self.hit_timer = 0
                self.change_state(States.STRIKE)
