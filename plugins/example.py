import time

from app_data.plugin_loader import Plugin


class Example(Plugin):
    def __init__(self, app):
        super().__init__(app)
        print("Example plugin initialized")

    def update(self, state_manager, time):
        print("Example plugin updated", state_manager, time)

    def send_updates(self):
        return {"example": "Bob"}


class ExamplePlugin2(Plugin):
    def __init__(self, app):
        super().__init__(app)
        print("Example plugin 2 initialized")

    def update(self, example):
        print("Example plugin 2 updated", example)

    def send_updates(self):
        return {"time": time.time()}


def setup(app):
    return [Example(app), ExamplePlugin2(app)]
