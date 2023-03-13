import state_manager
import plugin_loader
import event_handler


class App:
    def __init__(self, temporary_states = None, global_states = None, events = None):
        self.plugin_loader = plugin_loader.PluginLoader()
        self.event_handler = event_handler.EventHandler(
                events
        )
        self.state_manager = state_manager.StateManager(
                temporary_states,
                global_states
        )

        self.plugin_loader.load(self, 'plugins.example')
        self.event_handler.update('on_init', self)

    def update(self, *args, **kwargs):
        self.plugin_loader.update(*args, **kwargs)
        self.event_handler.update('on_update', *args, **kwargs)


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

    while True:
        app.update()
