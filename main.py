"""
Main entry point for GestureFlow.
"""

import cv2
import time
from src.camera.camera_manager import CameraManager
from src.hand_tracking.hand_detector import HandDetector
from src.mouse.air_mouse import AirMouse
from src.gestures.gesture_recognizer import GestureRecognizer


def main():
    prev_time = 0

    camera = CameraManager()
    detector = HandDetector()
    air_mouse = AirMouse()
    recognizer = GestureRecognizer()

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

            if recognizer.is_pinch(hand, w, h):
                print("LEFT CLICK")

            air_mouse.move_cursor(x, y)

        # ------------------------------------------ #

        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
        prev_time = curr_time

        cv2.putText(
            frame,
            f"FPS: {int(fps)}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2,
        )

        cv2.imshow("GestureFlow Webcam", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()

if __name__ == "__main__":
    main()
