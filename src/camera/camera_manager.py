"""
camera_manager.py
Handles all webcam-related operations for GestureFlow.

Author: Team GestureFlow
Project: GestureFlow
"""

import cv2
class CameraManager:
    """
    A class responsible for managing webcam operations.
    """

    def __init__(self, camera_index=0, mirror=True):
        """
        Initialize the webcam.

        Parameters:
            camera_index (int): Camera device index (default = 0)
        """
        self.camera = cv2.VideoCapture(camera_index)
        self.mirror = mirror

        if not self.camera.isOpened():
            raise RuntimeError("Unable to access the webcam.")

    def get_frame(self):
        """
        Capture and return a single frame.
        Returns:
            tuple: (success, frame)
        """

        success, frame = self.camera.read()
        if not success:
            return False, None

        if self.mirror:
            frame = cv2.flip(frame, 1)
        return True, frame

    def release(self):
        """
        Release the webcam safely.
        """
        self.camera.release()
        cv2.destroyAllWindows()