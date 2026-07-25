import pyautogui
import numpy as np


class AirMouse:
    def __init__(self):

        # Screen Resolution
        self.screen_width, self.screen_height = pyautogui.size()

        # Camera Resolution (Update if your webcam resolution changes)
        self.cam_width = 640
        self.cam_height = 480

        # Frame Reduction
        self.frame_margin = 100

        # Smoothing
        self.smoothening = 7

        # Previous Mouse Location
        self.prev_x = 0
        self.prev_y = 0

        # Current Mouse Location
        self.curr_x = 0
        self.curr_y = 0

    def move_cursor(self, x, y):

        # Convert Camera Coordinates → Screen Coordinates
        screen_x = np.interp(
            x,
            (self.frame_margin, self.cam_width - self.frame_margin),
            (0, self.screen_width),
        )

        screen_y = np.interp(
            y,
            (self.frame_margin, self.cam_height - self.frame_margin),
            (0, self.screen_height),
        )

        # Smooth Movement
        self.curr_x = self.prev_x + (screen_x - self.prev_x) / self.smoothening
        self.curr_y = self.prev_y + (screen_y - self.prev_y) / self.smoothening

        pyautogui.moveTo(self.curr_x, self.curr_y)

        self.prev_x = self.curr_x
        self.prev_y = self.curr_y