import os
import time
import pygame

from src.utils import BASE_PATH


class Animation:
    def __init__(self, dir_path, frame_rate, loop=True):
        """
        Animation class constructor
        :param dir_path: path to the directory containing the frames
        :param frame_rate: the time between each frame
        :param loop: if the animation should loop
        """

        # load the frames from the directory and set the initial values
        self.frame_list = self.load_frames(dir_path)
        self.current_frame = 0
        self.frame_rate = frame_rate
        self.last_update_time = time.time()
        self.loop = loop
        self.active = True

    @staticmethod
    def load_frames(dir_path) -> list[pygame.Surface]:
        """
        Load the frames from the directory
        :param dir_path: path to the directory containing the frames
        :return: list of frames [pygame.Surface]
        """
        # get the path to the directory and set the frames list
        dir_path = f"{BASE_PATH}/../{dir_path}"
        frames = []

        # load the frames from the directory
        for file in os.listdir(dir_path):
            if file.endswith(".png"):
                img = pygame.image.load(os.path.join(dir_path, file))
                img = pygame.transform.scale_by(img, 2).convert()
                img.set_colorkey((0, 0, 0))
                frames.append(img)

        # return the frames list
        return frames

    def update(self):
        """
        Update animation
        :return:
        """

        # if the animation is active, update the current frame
        if self.active:
            current_time = time.time()

            # if the time between the last update and the current time is greater than the frame rate update the frame
            if current_time - self.last_update_time >= self.frame_rate:

                # if the animation is not loop and the current frame is the last frame, set the current frame to 0
                if not self.loop and self.current_frame == len(self.frame_list) - 1:
                    self.current_frame = 0
                    self.active = False

                # if the animation is loop, update the current frame
                else:
                    self.current_frame = (self.current_frame + 1) % len(self.frame_list)
                    self.last_update_time = current_time

    def get_current_frame(self, direction):
        """
        Get the current frame
        :param direction: the direction of the animation ("right" or "left")
        :return: the current frame (pygame.Surface)
        """
        if direction == "right":
            return self.frame_list[self.current_frame]
        if direction == "left":
            return pygame.transform.flip(self.frame_list[self.current_frame], True, False)

    def end(self):
        """
        End the animation, set the current frame to 0 and active to True for the next time it is called
        :return:
        """
        self.current_frame = 0
        self.active = True
