import ctypes
import sdl2

from rendrer import Renderer


class Window:
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 800

    def __init__(self, title, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
        self.sdl_window = sdl2.SDL_CreateWindow(
            title,
            sdl2.SDL_WINDOWPOS_CENTERED,
            sdl2.SDL_WINDOWPOS_CENTERED,
            width,
            height,
            sdl2.SDL_WINDOW_RESIZABLE
        )
        self._renderer = Renderer(self)
        self.resize()

    @property
    def size(self):
        width = ctypes.c_int()
        height = ctypes.c_int()
        sdl2.SDL_GetWindowSize(self.sdl_window, ctypes.byref(width), ctypes.byref(height))
        return width.value, height.value

    def resize(self):
        self._renderer.resize()

    def on_key_pressed(self, key_code):
        self._renderer.on_key_pressed(key_code)

    def on_key_up(self, key_code):
        self._renderer.on_key_up(key_code)

    def close(self):
        sdl2.SDL_DestroyWindow(self.sdl_window)
        sdl2.SDL_Quit()

