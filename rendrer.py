import sdl2
import datetime

from canvas.canvas import Canvas
from polygon_mesh.cubes_mesh import CubesMesh


class Renderer:
    WHITE_COLOR = (255, 255, 255, 255)
    BLACK_COLOR = (0, 0, 0, 255)

    def __init__(self, window):
        self._window = window
        self.sdl_renderer = sdl2.SDL_CreateRenderer(
            self._window.sdl_window,
            -1,
            sdl2.SDL_RENDERER_ACCELERATED
        )
        self._canvas = Canvas(self)
        self._cubes = CubesMesh()

    @property
    def size(self):
        return self._window.size

    def resize(self):
        # d = datetime.datetime.now()
        self.redraw()
        # print(datetime.datetime.now() - d)

    def redraw(self):
        self._canvas.clear()
        self._draw_mesh()
        self._render_canvas_texture()

    def on_key_pressed(self, key_code):
        if key_code == 120:
            self._cubes.rotate(0.1, 0, 0)
        elif key_code == 121:
            self._cubes.rotate(0, 0.1, 0)
        elif key_code == 122:
            self._cubes.rotate(0, 0, 0.1)
        self.redraw()

    def _draw_mesh(self):
        for point_a, point_b, point_c, point_d in self._cubes.faces():
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

