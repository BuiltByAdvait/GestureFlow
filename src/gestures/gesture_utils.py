import math


class GestureUtils:
    @staticmethod
    def distance(point1, point2):
        """
        Returns the Euclidean distance between two landmarks.
        """

        x1, y1 = point1.x, point1.y
        x2, y2 = point2.x, point2.y

        return math.hypot(x2 - x1, y2 - y1)

    @staticmethod
    def pixel_distance(point1, point2, frame_width, frame_height):
        """
        Returns the distance in pixels.
        """

        x1 = point1.x * frame_width
        y1 = point1.y * frame_height

        x2 = point2.x * frame_width
        y2 = point2.y * frame_height

        return math.hypot(x2 - x1, y2 - y1)