from plugin_loader import Plugin


class Example(Plugin):
    def __init__(self, app):
        super().__init__(app)
        print("Example plugin initialized")



def setup(app):
    return [Example(app)]
