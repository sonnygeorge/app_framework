import state_manager
import plugin_loader
import event_handler


class App:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return getattr(cls, 'instance')

    def __init__(self, temporary_states = None, global_states = None, events = None):
        self.plugin_loader = plugin_loader.PluginLoader()
        self.event_handler = event_handler.EventHandler(
                events
        )
        self.state_manager = state_manager.StateManager(
                temporary_states,
                global_states
        )
        self.plugin_loader.load_modules(self)

    def update(self):
        self.plugin_loader.update(self.state_manager)

    def loop(self):
        while True:
            self.update()


if __name__ == '__main__':
    app = App(
            temporary_states = {
                    'temp_example': 0
            },
            global_states = {
                    'temp_example': 0
            },
            events = [
                    'on_init',
                    'on_update'
            ]
    )

    app.loop()
