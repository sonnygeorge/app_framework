from app_data import plugin_loader, state_manager
from app_data.app_logger import logger


class App:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return getattr(cls, 'instance')

    def __init__(self):
        self.plugin_loader = plugin_loader.PluginLoader()
        self.running = True

    def update(self):
        self.plugin_loader.update(state_manager.State.get_states())

    def run(self):
        self.plugin_loader.load_modules()
        while self.running:
            self.update()
        for plugin_name in self.plugin_loader.plugins:
            self.plugin_loader.unload(plugin_name)
        logger.info("App exited")


if __name__ == '__main__':
    app = App()
    app.run()
