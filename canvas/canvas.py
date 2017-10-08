from math import trunc

from canvas.canvas_point import CanvasPoint
from canvas.line_drawer import LineDrawer


class Canvas:
    BLANK_POINT = CanvasPoint(float('-inf'), (255, 255, 255, 255))

    def __init__(self, renderer):
        self._width, self._height = renderer.size
        self.texture = []
        self.clear()

    def draw_line(self, point_a, point_b):
        LineDrawer(self,  *point_a, *point_b).draw()

    def clear(self):
        self.texture = [
            [self.BLANK_POINT] * self._width for _ in range(self._height)
        ]

    def draw_point(self, x, y, z, is_dash=False, color=(0, 0, 0, 255)):
        point_in_canvas = 0 <= x <= self._width and 0 <= y <= self._height
        if point_in_canvas and (self.texture[x][y].z_index < z or is_dash):
            self.texture[x][y] = CanvasPoint(z, color)

    def draw_rect(self, point_a, point_b, point_c, point_d, color):
        self._draw_triangle(point_a, point_b, point_c, color)
        self._draw_triangle(point_c, point_d, point_a, color)

    def _draw_triangle(self, point_a, point_b, point_c, color):
        if point_a[1] > point_b[1]:
            point_a, point_b = point_b, point_a
        if point_b[1] > point_c[1]:
            point_b, point_c = point_c, point_b
        if point_a[1] > point_b[1]:
            point_a, point_b = point_b, point_a
        d_a_b = (point_b[0] - point_a[0]) / (point_b[1] - point_a[1]) if point_b[1] - point_a[1] > 0 else 0
        d_a_c = (point_c[0] - point_a[0]) / (point_c[1] - point_a[1]) if point_c[1] - point_a[1] > 0 else 0
        if d_a_b > d_a_c:
            for y in range(trunc(point_a[1]), trunc(point_c[1])):
                if y < point_b[1]:
                    self._process_scan_line(y, point_a, point_c, point_a, point_b, color)
                else:
                    self._process_scan_line(y, point_a, point_c, point_b, point_c, color)
        else:
            for y in range(trunc(point_a[1]), trunc(point_c[1])):
                if y < point_b[1]:
                    self._process_scan_line(y, point_a, point_b, point_a, point_c, color)
                else:
                    self._process_scan_line(y, point_b, point_c, point_a, point_c, color)

    def _process_scan_line(self, y, point_a, point_b, point_c, point_d, color):
        x_a, y_a, z_a = point_a
        x_b, y_b, z_b = point_b
        x_c, y_c, z_c = point_c
        x_d, y_d, z_d = point_d
        gradient1 = (y - y_a) / (y_b - y_a) if y_a != y_b else 1
        gradient2 = (y - y_c) / (y_d - y_c) if y_c != y_d else 1
        sx = round(self._interpolate(x_a, x_b, gradient1))
        ex = round(self._interpolate(x_c, x_d, gradient2))
        z1 = self._interpolate(z_a, z_b, gradient1)
        z2 = self._interpolate(z_c, z_d, gradient2)
        for x in range(sx, ex):
            gradient = (x - sx) / (ex - sx)
            z = self._interpolate(z1, z2, gradient)
            self.draw_point(x, y, z, color=color)

    def _interpolate(self, minimum, maximum, gradient):
        return minimum + (maximum - minimum) * self._clamp(gradient)

    def _clamp(self, value):
        return max(0, min(value, 1))


