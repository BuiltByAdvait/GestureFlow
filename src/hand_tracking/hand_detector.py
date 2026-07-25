import cv2
from mediapipe.python.solutions import hands
from mediapipe.python.solutions import drawing_utils
from src.gestures.gesture_recognizer import GestureRecognizer


class HandDetector:
    def __init__(
        self,
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
    ):

        self.mp_hands = hands
        self.hands = hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

        self.drawer = drawing_utils
        self.recognizer = GestureRecognizer()

    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb)

        if self.results.multi_hand_landmarks:
            for hand, handedness in zip(
                self.results.multi_hand_landmarks,
                self.results.multi_handedness
            ):
                self.drawer.draw_landmarks(
                    frame,
                    hand,
                    self.mp_hands.HAND_CONNECTIONS,
                )

                hand_label = handedness.classification[0].label
                gesture, fingers, total = self.recognizer.recognize(
                    hand,
                    hand_label,
                )
                cv2.putText(
                    frame,
                    f"{hand_label} : {gesture} ({total})",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )
        return frame