import sdl2
import datetime
from math import trunc

from canvas.canvas import Canvas
from polygon_mesh.cubes_mesh import CubesMesh


class Renderer:
    WHITE_COLOR = (255, 255, 255, 255)
    BLACK_COLOR = (0, 0, 0, 255)
    X_CODE = 120
    Y_CODE = 121
    Z_CODE = 122
    P_CODE = 112
    R_CODE = 114
    E_CODE = 101
    D_CODE = 100
    L_SHIFT_CODE = 1073742049

    def __init__(self, window):
        self._window = window
        self.sdl_renderer = sdl2.SDL_CreateRenderer(
            self._window.sdl_window,
            -1,
            sdl2.SDL_RENDERER_ACCELERATED
        )
        self._canvas = Canvas(self)
        self._cubes = CubesMesh(self.size[1])
        self.grow_step = 0.1

    @property
    def size(self):
        return self._window.size

    def resize(self):
        self.redraw()

    def redraw(self):
        # d = datetime.datetime.now()
        self._canvas.clear()
        # print(datetime.datetime.now() - d)
        self._draw_mesh()
        # print(datetime.datetime.now() - d)
        self._render_canvas_texture()
        # print(datetime.datetime.now() - d)

    def on_key_pressed(self, key_code):
        if key_code == self.X_CODE:
            self._cubes.rotate(self.grow_step, 0, 0)
        elif key_code == self.Y_CODE:
            self._cubes.rotate(0, self.grow_step, 0)
        elif key_code == self.Z_CODE:
            self._cubes.rotate(0, 0, self.grow_step)
        elif key_code == self.P_CODE:
            self._cubes.rotate_camera(phi=self.grow_step)
        elif key_code == self.E_CODE:
            self._cubes.rotate_camera(etha=self.grow_step)
        elif key_code == self.R_CODE:
            self._cubes.rotate_camera(distance=self.grow_step * 1000)
        elif key_code == self.D_CODE:
            self._cubes.change_perspective(self.grow_step / 10)
        elif key_code == self.L_SHIFT_CODE:
            self.grow_step = -self.grow_step
        else:
            return
        self.redraw()

    def on_key_up(self, key_code):
        if key_code == self.L_SHIFT_CODE:
            self.grow_step = -self.grow_step

    def _draw_mesh(self):
        for index, points in enumerate(self._cubes.faces()):
            k_for_color = index // 6
            if k_for_color == 0:
                color_rgba = (0, 0, 255, 255)
            elif k_for_color == 1:
                color_rgba = (0, 255, 0, 255)
            else:
                color_rgba = (255, 0, 0, 255)

            point_a, point_b, point_c, point_d = points
            self._canvas.draw_rect(point_a, point_b, point_c, point_d, color_rgba)

            self._canvas.draw_line(point_a, point_b)
            self._canvas.draw_line(point_b, point_c)
            self._canvas.draw_line(point_c, point_d)
            self._canvas.draw_line(point_d, point_a)

    def _render_canvas_texture(self):
        self._clear_draw_field()
        for x, x_row in enumerate(self._canvas.texture):
            for y, pixel_info in enumerate(x_row):
                color = pixel_info.color
                if color != self.WHITE_COLOR:
                    sdl2.SDL_SetRenderDrawColor(self.sdl_renderer, *pixel_info.color)
                    sdl2.SDL_RenderDrawPoint(self.sdl_renderer, x, y)
        sdl2.SDL_RenderPresent(self.sdl_renderer)

    def _clear_draw_field(self):
        sdl2.SDL_SetRenderDrawColor(self.sdl_renderer, *self.WHITE_COLOR)
        sdl2.SDL_RenderClear(self.sdl_renderer)
        sdl2.SDL_SetRenderDrawColor(self.sdl_renderer, *self.BLACK_COLOR)

