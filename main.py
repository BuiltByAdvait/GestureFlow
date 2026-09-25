"""
    Main entry point for GestureFlow.
"""

import cv2
import time
from src.camera.camera_manager import CameraManager
from src.hand_tracking.hand_detector import HandDetector
from src.mouse.air_mouse import AirMouse
from src.gestures.gesture_recognizer import GestureRecognizer
from src.canvas.air_canvas import AirCanvas


def main():
    prev_time = 0

    camera = CameraManager()
    detector = HandDetector()
    air_mouse = AirMouse()
    recognizer = GestureRecognizer()
    air_canvas = AirCanvas()

    while True:
        success, frame = camera.get_frame()
        if not success:
            print("Failed to capture frame.")
            break
        frame = detector.detect(frame)

        # ---------------- AIR MOUSE ---------------- #
        if detector.results.multi_hand_landmarks:

            hand = detector.results.multi_hand_landmarks[0]

            gesture, fingers, total = recognizer.recognize(
                hand,
                detector.results.multi_handedness[0].classification[0].label
            )

            index_tip = hand.landmark[8]
            
            h, w, _ = frame.shape

            x = int(index_tip.x * w)
            y = int(index_tip.y * h)

            # Recognize hand gesture
            hand_label = "Right"

            if detector.results.multi_handedness:
                hand_label = (
                    detector.results.multi_handedness[0]
                    .classification[0]
                    .label
                )

            gesture, fingers, total = recognizer.recognize(
                hand,
                hand_label,
            )

            click_action = recognizer.is_pinch(hand, w, h)

            frame = air_canvas.update(
                frame,
                hand,
                gesture,
                recognizer.is_pinching
            )
            
            right_click = recognizer.is_right_click(hand, w, h)

            scroll_direction = recognizer.get_scroll_direction(hand, h)

            if click_action == 1:
                air_mouse.left_click()
                print("LEFT CLICK")

            elif click_action == 2:
                air_mouse.double_click()
                print("DOUBLE CLICK")

            elif right_click:
                air_mouse.right_click()
                print("RIGHT CLICK")

            elif scroll_direction > 0:
                air_mouse.scroll(scroll_direction)

            elif scroll_direction < 0:
                air_mouse.scroll(scroll_direction)


            # Freeze cursor while clicking
            if (
                click_action == 0
                and not recognizer.is_pinching
                and not right_click
                and not recognizer.scroll_active
            ):
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
