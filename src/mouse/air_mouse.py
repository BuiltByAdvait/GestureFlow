import pyautogui
import numpy as np

pyautogui.PAUSE = 0

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
        # Cursor Smoothing
        self.smoothening = 5

        # Ignore very tiny movements
        self.dead_zone = 6

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

        # -----------------------------
        # Dead Zone
        # -----------------------------
        if (
            abs(screen_x - self.prev_x) < self.dead_zone
            and abs(screen_y - self.prev_y) < self.dead_zone
        ):
            return

        # -----------------------------
        # Dynamic Smoothing
        # -----------------------------
        distance = np.hypot(
            screen_x - self.prev_x,
            screen_y - self.prev_y,
        )

        if distance < 40:
            smoothing = 8
        elif distance < 100:
            smoothing = 5
        else:
            smoothing = 3

        self.curr_x = self.prev_x + (
            screen_x - self.prev_x
        ) / smoothing

        self.curr_y = self.prev_y + (
            screen_y - self.prev_y
        ) / smoothing

        # -----------------------------
        # Keep cursor inside screen
        # -----------------------------
        self.curr_x = np.clip(
            self.curr_x,
            0,
            self.screen_width - 1,
        )

        self.curr_y = np.clip(
            self.curr_y,
            0,
            self.screen_height - 1,
        )

        pyautogui.moveTo(
            self.curr_x,
            self.curr_y,
            duration = 0
        )

        self.prev_x = self.curr_x
        self.prev_y = self.curr_y