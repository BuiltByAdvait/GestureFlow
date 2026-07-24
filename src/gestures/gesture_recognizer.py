class GestureRecognizer:
    FINGER_TIPS = [4, 8, 12, 16, 20]

    def __init__(self):
        pass

    def recognize(
        self,
        hand_landmarks,
        hand_label,
    ):
        landmarks = hand_landmarks.landmark
        fingers = []

        # Thumb
        if hand_label == "Right":
            if landmarks[4].x < landmarks[3].x:
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            if landmarks[4].x > landmarks[3].x:
                fingers.append(1)
            else:
                fingers.append(0)

        # Index
        if landmarks[8].y < landmarks[6].y:
            fingers.append(1)
        else:
            fingers.append(0)

        # Middle
        if landmarks[12].y < landmarks[10].y:
            fingers.append(1)
        else:
            fingers.append(0)

        # Ring
        if landmarks[16].y < landmarks[14].y:
            fingers.append(1)
        else:
            fingers.append(0)

        # Pinky
        if landmarks[20].y < landmarks[18].y:
            fingers.append(1)
        else:
            fingers.append(0)

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