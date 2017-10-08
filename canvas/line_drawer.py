# Attention! Optimized code below! Take care of your eyes.
class LineDrawer:
    DASH_LENGTH = 2

    def __init__(self, canvas, x1, y1, z1, x2, y2, z2):
        self._canvas = canvas
        self._x1, self._y1, self._z1 = round(x1), round(y1), z1
        x2, y2, z2 = round(x2), round(y2), z2
        self._delta_x = abs(x2 - self._x1)
        self._delta_y = abs(y2 - self._y1)
        self._delta_z = abs(z2 - self._z1)
        self._step_x = 1 if x2 >= self._x1 else -1
        self._step_y = 1 if y2 >= self._y1 else -1
        self._step_z = 1 if z2 >= self._z1 else -1
        self._d2 = -abs(self._delta_x - self._delta_y) * 2

    def draw(self):
        if self._delta_x >= self._delta_y:
            self._draw_by_continuous_x_increase(self._x1, self._y1, self._z1)
        else:
            self._draw_by_continuous_y_increase(self._x1, self._y1, self._z1)

    def _draw_by_continuous_x_increase(self, x, y, z):
        d1 = self._delta_y * 2
        d = d1 - self._delta_x
        dz = 0 if self._delta_x == 0 else (self._delta_z / self._delta_x)
        for i in range(self._delta_x):
            self._draw_point(x, y, z, i)
            x += self._step_x
            z += dz * self._step_z
            if d > 0:
                d += self._d2
                y += self._step_y
            else:
                d += d1

    def _draw_by_continuous_y_increase(self, x, y, z):
        d1 = self._delta_x * 2
        d = d1 - self._delta_y
        dz = 0 if self._delta_x == 0 else (self._delta_z / self._delta_y)
        for i in range(self._delta_y):
            self._draw_point(x, y, z, i)
            y += self._step_y
            z += dz * self._step_z
            if d > 0:
                d += self._d2
                x += self._step_x
            else:
                d += d1

    def _is_draw_dash_point(self, point_index):
        return point_index % (self.DASH_LENGTH * 2) > self.DASH_LENGTH

    def _draw_point(self, x, y, z, point_index):
        self._canvas.draw_point(x, y, z, is_dash=self._is_draw_dash_point(point_index))
