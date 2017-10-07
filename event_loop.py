import ctypes

import sdl2

from event_dispatcher import EventDispatcher


class EventLoop:
    def __init__(self, window):
        self._event_dispatcher = EventDispatcher(self, window)
        self._running = False

    def run(self):
        self._running = True
        while self._running:
            self._receive_events()

    def stop(self):
        self._running = False

    def _receive_events(self):
        event = sdl2.SDL_Event()
        event_pointer = ctypes.byref(event)
        while self._running and sdl2.SDL_PollEvent(event_pointer) != 0:
            self._event_dispatcher.dispatch(event)

