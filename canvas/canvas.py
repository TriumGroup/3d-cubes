from math import trunc

from canvas.canvas_point import CanvasPoint
from canvas.line_drawer import LineDrawer


class Canvas:
    EMPTY_POINT = CanvasPoint(float('-inf'), (255, 255, 255, 255))

    def __init__(self, renderer):
        self._width, self._height = renderer.size
        self.texture = []
        self.clear()

    def draw_line(self, point_a, point_b):
        LineDrawer(self,  *point_a, *point_b).draw()

    def clear(self):
        self.texture = [
            [self.EMPTY_POINT for _ in range(self._width)] for _ in range(self._height)
        ]

    def draw_point(self, x, y, z, is_dash=False, color=(0, 0, 0, 255)):
        point_in_canvas = 0 <= x <= self._width and 0 <= y <= self._height
        if point_in_canvas and (self.texture[x][y].z_index < z or is_dash):
            self.texture[x][y] = CanvasPoint(z, color)