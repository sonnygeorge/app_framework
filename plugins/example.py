from app_data.plugin_loader import Plugin


class Example(Plugin):
    def __init__(self, app):
        super().__init__(app)
        print("Example plugin initialized")

    def update(self, state_manager):
        print("Example plugin updated", state_manager)


class ExamplePlugin2(Plugin):
    def __init__(self, app):
        super().__init__(app)
        print("Example plugin 2 initialized")

    def update(self):
        print("Example plugin 2 updated")

def setup(app):
    return [Example(app), ExamplePlugin2(app)]
