from app_data import plugin_loader, state_manager, event_handler


class App:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return getattr(cls, 'instance')

    def __init__(self, temporary_states = None, global_states = None, events = None):
        self.plugin_loader = plugin_loader.PluginLoader(

        )
        self.event_handler = event_handler.EventHandler(
                events
        )
        self.state_manager = state_manager.StateManager(
                temporary_states or {},
                global_states or {}
        )
        self.plugin_loader.load_modules(self)

    def update(self, **kwargs):
        self.plugin_loader.update(**kwargs)

    def loop(self):
        while True:
            self.update(state_manager = self.state_manager, **self.update_parameters())

    def update_parameters(self) -> dict:  # noqa
        """Override this functions to add custom params to the update loop"""
        return {}


if __name__ == '__main__':
    app = App(

    )

    app.loop()
