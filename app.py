from app_data import plugin_loader, state_manager
from app_data.app_logger import logger


class App:
    """Main App class, this coordinates the other features of the app.
    Is the only source of coupling between the other modules, barring the logger."""
    def __new__(cls, *args, **kwargs):
        """Singleton pattern"""
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return getattr(cls, 'instance')

    def __init__(self):
        """Initializes the app, loads the plugin loader and sets the running flag to true."""
        self.plugin_loader = plugin_loader.PluginLoader()
        self.running = True

    def update(self):
        """Updates the app, this is the main loop of the app, gets the states from the state manager and updates the plugins."""
        self.plugin_loader.update(state_manager.State.get_states())

    def run(self):
        """Runs the app, this is the main entry point of the app, it loads the plugins and runs the main loop."""
        self.plugin_loader.load_modules()
        while self.running:
            self.update()
        for plugin_name in self.plugin_loader.plugins:
            self.plugin_loader.unload(plugin_name)
        logger.info("App exited")


if __name__ == '__main__':
    app = App()
    app.run()
