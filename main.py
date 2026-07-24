"""
Main entry point for GestureFlow.
"""

import cv2
from src.camera.camera_manager import CameraManager
from src.hand_tracking.hand_detector import HandDetector


def main():
    camera = CameraManager()
    detector = HandDetector()

    while True:
        success, frame = camera.get_frame()
        frame = detector.detect(frame)
        if not success:
            print("Failed to capture frame.")
            break

        cv2.imshow("GestureFlow Webcam", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()

if __name__ == "__main__":
    main()