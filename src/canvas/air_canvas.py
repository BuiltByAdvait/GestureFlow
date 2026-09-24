import cv2
import numpy as np
import time


class AirCanvas:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height

        # White drawing canvas
        self.canvas = np.ones(
            (height, width, 3),
            dtype=np.uint8
        ) * 255

        # Current drawing settings
        self.color = (0, 0, 255)  # Red
        self.brush_size = 5
        self.eraser_size = 30

        # Previous fingertip position
        self.prev_point = None

        # Current mode
        self.drawing = False
        self.eraser = False

        # Toolbar selection tracking
        self.selection_point = None
        self.selection_active = False

        # Available colors
        self.colors = [
            ("RED", (0, 0, 255)),
            ("BLUE", (255, 0, 0)),
            ("GREEN", (0, 180, 0)),
            ("BLACK", (0, 0, 0)),
        ]

        # Available brush sizes
        self.brush_sizes = [3, 7, 12]

        # Toolbar settings
        self.toolbar_height = 70

        # Message shown after saving
        self.save_message = ""
        self.save_message_time = 0

    def reset_point(self):
        """Stop the current stroke."""
        self.prev_point = None

    def draw(self, point):
        """Draw a smooth line from the previous point to the current point."""

        if self.prev_point is None:
            self.prev_point = point
            return

        x1, y1 = self.prev_point
        x2, y2 = point

        if self.eraser:
            cv2.line(
                self.canvas,
                (x1, y1),
                (x2, y2),
                (255, 255, 255),
                self.eraser_size,
                cv2.LINE_AA,
            )
        else:
            cv2.line(
                self.canvas,
                (x1, y1),
                (x2, y2),
                self.color,
                self.brush_size,
                cv2.LINE_AA,
            )

        self.prev_point = point

    def draw_toolbar(self, frame):
        """Draw the Air Canvas toolbar."""

        cv2.rectangle(
            frame,
            (0, 0),
            (self.width, self.toolbar_height),
            (40, 40, 40),
            -1,
        )

        # Colors
        x = 10

        for name, color in self.colors:
            cv2.rectangle(
                frame,
                (x, 10),
                (x + 40, 50),
                color,
                -1,
            )

            if color == self.color and not self.eraser:
                cv2.rectangle(
                    frame,
                    (x - 2, 8),
                    (x + 42, 52),
                    (255, 255, 255),
                    2,
                )

            x += 50

        # Brush sizes
        cv2.putText(
            frame,
            "SIZE",
            (220, 32),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )

        x = 275

        for size in self.brush_sizes:
            cv2.circle(
                frame,
                (x, 30),
                max(size, 4),
                (255, 255, 255),
                -1,
            )

            if size == self.brush_size and not self.eraser:
                cv2.circle(
                    frame,
                    (x, 30),
                    15,
                    (255, 255, 255),
                    2,
                )

            x += 45

        # Eraser
        cv2.rectangle(
            frame,
            (420, 10),
            (490, 50),
            (100, 100, 100),
            -1,
        )

        cv2.putText(
            frame,
            "ERASE",
            (425, 37),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 255, 255),
            1,
        )

        # Clear
        cv2.rectangle(
            frame,
            (500, 10),
            (555, 50),
            (100, 100, 100),
            -1,
        )

        cv2.putText(
            frame,
            "CLEAR",
            (503, 37),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.42,
            (255, 255, 255),
            1,
        )

        # Save
        cv2.rectangle(
            frame,
            (565, 10),
            (625, 50),
            (100, 100, 100),
            -1,
        )

        cv2.putText(
            frame,
            "SAVE",
            (570, 37),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 255, 255),
            1,
        )

    def handle_selection(self, x, y):
        """Handle toolbar selection using the stored fingertip position."""

        if y > self.toolbar_height:
            return

        # Color buttons
        for i, (_, color) in enumerate(self.colors):
            x1 = 10 + i * 50
            x2 = x1 + 40

            if x1 <= x <= x2 and 5 <= y <= 60:
                self.color = color
                self.eraser = False
                return

        # Brush sizes
        for i, size in enumerate(self.brush_sizes):
            center_x = 275 + i * 45

            if abs(x - center_x) <= 25 and 5 <= y <= 60:
                self.brush_size = size
                self.eraser = False
                return

        # Eraser
        if 410 <= x <= 500 and 5 <= y <= 60:
            self.eraser = True
            return

        # Clear
        if 490 <= x <= 565 and 5 <= y <= 60:
            self.clear()
            return

        # Save
        if 555 <= x <= 635 and 5 <= y <= 60:
            self.save()

    def clear(self):
        """Clear the entire drawing."""
        self.canvas[:] = 255
        self.reset_point()

    def save(self):
        """Save the current drawing as a PNG."""
        filename = "air_canvas.png"
        cv2.imwrite(filename, self.canvas)

        self.save_message = f"Saved: {filename}"
        self.save_message_time = time.time()

    def update(self, frame, hand, gesture, recognizer):
        """
        Update the Air Canvas using the existing MediaPipe hand.

        ONE  -> draw
        TWO  -> selection mode
        FIST -> pause
        """

        h, w, _ = frame.shape

        self.width = w
        self.height = h

        # Draw toolbar
        self.draw_toolbar(frame)

        # Show the drawing on the webcam frame
        frame = cv2.addWeighted(
            frame,
            0.7,
            self.canvas,
            0.3,
            0
        )

        if hand is None:
            self.reset_point()
            return frame

        # Existing MediaPipe index fingertip
        index_tip = hand.landmark[8]

        x = int(index_tip.x * w)
        y = int(index_tip.y * h)

        # Keep fingertip inside frame
        x = max(0, min(x, w - 1))
        y = max(0, min(y, h - 1))

        # TWO fingers = selection mode
        if gesture == "TWO":

            self.reset_point()

            cv2.circle(
                frame,
                (x, y),
                12,
                (0, 255, 255),
                2,
            )

            # Check if thumb and index finger are pinched
            pinching = recognizer.is_pinch(hand, w, h)

            # Remember the fingertip position before the pinch
            if not pinching:
                self.selection_point = (x, y)
                self.selection_active = False

            # Use the remembered position when pinch happens
            if pinching:
                if (
                    self.selection_point is not None
                    and not self.selection_active
                ):
                    sx, sy = self.selection_point
                    self.handle_selection(sx, sy)
                    self.selection_active = True

        # ONE finger = drawing mode
        elif gesture == "ONE":

            # Don't draw over toolbar
            if y > self.toolbar_height:
                self.draw((x, y))

                cv2.circle(
                    frame,
                    (x, y),
                    8,
                    self.color if not self.eraser else (0, 0, 0),
                    -1,
                )
            else:
                self.reset_point()

        # Any other gesture = stop drawing
        else:
            self.reset_point()

        # Show save message
        if self.save_message:
            if time.time() - self.save_message_time < 2:
                cv2.putText(
                    frame,
                    self.save_message,
                    (20, h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 150, 0),
                    2,
                )
            else:
                self.save_message = ""

        return frame

    def get_canvas(self):
        """Return the current drawing."""
        return self.canvas.copy()