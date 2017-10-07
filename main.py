import sys

from event_loop import EventLoop
from window import Window


def main():
    window_with_plot = Window(b"Lab 4")
    EventLoop(window_with_plot).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
