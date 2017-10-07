import sdl2


class EventDispatcher:
    def __init__(self, event_loop, window):
        self._window = window
        self._event_loop = event_loop
        self._event_dispatchers = {
            sdl2.SDL_WINDOWEVENT: self._dispatch_window_event,
            sdl2.SDL_KEYDOWN: self._dispatch_keydown_event,
            sdl2.SDL_QUIT: self._dispatch_quit_event
        }

    def dispatch(self, event):
        dispatcher = self._event_dispatchers.get(event.type)
        if dispatcher is not None:
            dispatcher(event)

    def _dispatch_window_event(self, event):
        if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
            self._window.resize()

    def _dispatch_keydown_event(self, event):
        self._window.on_key_pressed(event.key.keysym.sym)

    def _dispatch_quit_event(self, _):
        self._event_loop.stop()
        self._window.close()
