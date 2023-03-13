from plugin_loader import Plugin
from event_handler import subscribe

class Example(Plugin):
    def __init__(self, app):
        super().__init__(app)
        print("Example plugin initialized")

    @subscribe(event = 'on_init')
    def on_init(self, app):
        print("Example plugin on_init event triggered")



def setup(app):
    return [Example(app)]
