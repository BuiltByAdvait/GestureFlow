"""
Main entry point for GestureFlow.
"""

import cv2
from src.camera.camera_manager import CameraManager
from src.hand_tracking.hand_detector import HandDetector
from src.mouse.air_mouse import AirMouse


def main():
    camera = CameraManager()
    detector = HandDetector()
    air_mouse = AirMouse()

    while True:
        success, frame = camera.get_frame()
        if not success:
            print("Failed to capture frame.")
            break
        frame = detector.detect(frame)

        # ---------------- AIR MOUSE ---------------- #
        if detector.results.multi_hand_landmarks:
            hand = detector.results.multi_hand_landmarks[0]
            index_tip = hand.landmark[8]
            
            h, w, _ = frame.shape

            x = int(index_tip.x * w)
            y = int(index_tip.y * h)

            air_mouse.move_cursor(x, y)

        # ------------------------------------------ #

        cv2.imshow("GestureFlow Webcam", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()

if __name__ == "__main__":
    main()