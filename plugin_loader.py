import pathlib, importlib, sys
from abc import ABC
import state_manager


class Plugin(ABC):
    def __init__(self, app, **states):
        self.app = app
        self.states = state_manager.GlobalStateEnum(self.__class__.__name__, states)

    def update(self):
        print("Plugin update")

    def unload(self):
        pass


class PluginLoader:
    plugins = dict()

    def __init__(self, plugin_path="plugins"):
        self.plugin_path = pathlib.Path(plugin_path)
        self.plugin_path.mkdir(parents=True, exist_ok=True)

    def load(self, app, module_name):
        module = importlib.import_module(module_name)
        plugins = module.setup(app)
        for plugin in plugins:
            self.plugins[getattr(plugin, "name", plugin.__class__.__name__)] = plugin

    def unload(self, module_name):
        for plugin in self.plugins.values():
            if plugin.__module__ == module_name:
                getattr(plugin, "unload", lambda: None)()
        del sys.modules[module_name]

    def update(self, *args, **kwargs):
        for plugin in self.plugins.values():
            plugin.update(*args, **kwargs)
