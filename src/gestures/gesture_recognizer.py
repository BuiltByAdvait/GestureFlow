import time
from src.gestures.gesture_utils import GestureUtils


class GestureRecognizer:
    FINGER_TIPS = [4, 8, 12, 16, 20]

    def __init__(self):
        # Click state
        self.is_pinching = False
        self.click_triggered = False

        # Double-click state
        self.pending_click = False
        self.pending_click_time = 0
        self.double_click_window = 0.4

        # Right-click state
        self.right_click_triggered = False

        # Scroll state
        self.scroll_active = False
        self.previous_scroll_y = None
        self.scroll_threshold = 12

    def recognize(self, hand_landmarks, hand_label):

        landmarks = hand_landmarks.landmark
        fingers = []

        # Thumb
        if hand_label == "Right":
            fingers.append(
                1 if landmarks[4].x < landmarks[3].x else 0
            )
        else:
            fingers.append(
                1 if landmarks[4].x > landmarks[3].x else 0
            )

        # Index
        fingers.append(
            1 if landmarks[8].y < landmarks[6].y else 0
        )

        # Middle
        fingers.append(
            1 if landmarks[12].y < landmarks[10].y else 0
        )

        # Ring
        fingers.append(
            1 if landmarks[16].y < landmarks[14].y else 0
        )

        # Pinky
        fingers.append(
            1 if landmarks[20].y < landmarks[18].y else 0
        )

        total = sum(fingers)

        gesture = "UNKNOWN"

        if fingers == [0, 0, 0, 0, 0]:
            gesture = "FIST"

        elif fingers == [0, 1, 0, 0, 0]:
            gesture = "ONE"

        elif fingers == [0, 1, 1, 0, 0]:
            gesture = "TWO"

        elif fingers == [0, 1, 1, 1, 0]:
            gesture = "THREE"

        elif fingers == [0, 1, 1, 1, 1]:
            gesture = "FOUR"

        elif fingers == [1, 1, 1, 1, 1]:
            gesture = "FIVE"

        return gesture, fingers, total

    def is_pinch(
        self,
        hand_landmarks,
        frame_width,
        frame_height,
    ):
        """
        Detects thumb + index pinch.

        Returns:
            0 -> No click action
            1 -> Single click
            2 -> Double click
        """

        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]

        distance = GestureUtils.pixel_distance(
            thumb_tip,
            index_tip,
            frame_width,
            frame_height,
        )

        PINCH_THRESHOLD = 35
        current_time = time.time()

        # Pinch start
        if distance < PINCH_THRESHOLD:

            # Trigger only once while fingers remain together
            if not self.click_triggered:

                self.click_triggered = True
                self.is_pinching = True

                # Second pinch within double-click window
                if (
                    self.pending_click
                    and current_time - self.pending_click_time
                    <= self.double_click_window
                ):
                    self.pending_click = False
                    return 2

                # First pinch
                self.pending_click = True
                self.pending_click_time = current_time

            return 0

        # Pinch release
        else:

            self.is_pinching = False
            self.click_triggered = False

            # First pinch was not followed by second pinch
            if (
                self.pending_click
                and current_time - self.pending_click_time
                > self.double_click_window
            ):
                self.pending_click = False
                return 1

        return 0

    def is_right_click(
        self,
        hand_landmarks,
        frame_width,
        frame_height,
    ):
        """
        Detects thumb + middle finger pinch.

        Returns:
            True -> Right click detected
            False -> No right click
        """

        thumb_tip = hand_landmarks.landmark[4]
        middle_tip = hand_landmarks.landmark[12]

        distance = GestureUtils.pixel_distance(
            thumb_tip,
            middle_tip,
            frame_width,
            frame_height,
        )

        RIGHT_CLICK_THRESHOLD = 35

        if distance < RIGHT_CLICK_THRESHOLD:

            if not self.right_click_triggered:
                self.right_click_triggered = True
                return True

        else:
            self.right_click_triggered = False

        return False

    def get_scroll_direction(
        self,
        hand_landmarks,
        frame_height,
    ):
        """
        Detects two-finger scroll mode.

        Returns:
            positive value -> Scroll Up
            negative value -> Scroll Down
            0 -> No scroll
        """

        landmarks = hand_landmarks.landmark

        # Detect TWO-FINGER gesture
        index_up = landmarks[8].y < landmarks[6].y
        middle_up = landmarks[12].y < landmarks[10].y

        ring_down = landmarks[16].y > landmarks[14].y
        pinky_down = landmarks[20].y > landmarks[18].y

        if not (
            index_up
            and middle_up
            and ring_down
            and pinky_down
        ):
            self.scroll_active = False
            self.previous_scroll_y = None
            return 0

        self.scroll_active = True

        # Current hand position
        current_y = (
            (landmarks[8].y + landmarks[12].y) / 2
        ) * frame_height

        # First frame
        if self.previous_scroll_y is None:
            self.previous_scroll_y = current_y
            return 0

        # Total movement
        movement = self.previous_scroll_y - current_y

        # Ignore tiny camera/hand jitter
        if abs(movement) < 6:
            return 0

        # Update reference
        self.previous_scroll_y = current_y

        # Convert movement to scroll
        scroll_amount = 1

        if movement > 0:
            return scroll_amount

        return -scroll_amount