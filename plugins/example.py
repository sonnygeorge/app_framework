from app_data.plugin_loader import Plugin
from app_data.event_handler import subscribe


class Example(Plugin):
    def __init__(self, app):
        super().__init__(app)
        print("Example plugin initialized")

    def update(self, *args, **kwargs):
        print("Example plugin update")

def setup(app):
    return [Example(app)]
