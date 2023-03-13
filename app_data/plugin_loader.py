import importlib
import inspect
import pathlib
from abc import ABC
import functools
from app_data.app_logger import logger


@functools.lru_cache
def get_func_params(func):
    """Returns a dict of the parameters of a function"""
    return inspect.signature(func).parameters


class Plugin(ABC):
    """Base class for plugins, all plugins should inherit from this class."""
    def __init__(self, name = None):
        """Initializes the plugin, sets the name of the plugin to the class name if no name is provided."""
        self.name = name
        logger.debug(f"Plugin {getattr(self, 'name', self.__class__.__name__)} initialized")

    def update(self, *args, **kwargs):
        """Updates the plugin, this is the main loop of the plugin, it is called every time the app updates.
        Uses an ipt in system for parameter, so it adds the parameters it needs and the plugin loader will pass them in.
        """
        ...

    def unload(self):
        """Unloads the plugin, this is called when the app is exiting."""
        ...


class PluginLoader:
    plugins = dict()

    def __new__(cls, *args, **kwargs):
        """Singleton pattern"""
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return getattr(cls, "instance")

    def __init__(self, plugin_path = "plugins"):
        """Initializes the plugin loader, sets the plugin path to the plugins folder in the current directory."""
        self.plugin_path = pathlib.Path(plugin_path)
        self.plugin_path.mkdir(parents = True, exist_ok = True)

    def load_module(self,  module):
        """Loads a module, this is used to load a module from the plugin path, it imports the module and calls the setup function."""
        module = importlib.import_module(module)
        plugins = module.setup()
        for plugin in plugins:
            self.load(plugin)

    def load_modules(self):
        """Loads all modules, this is used to load all modules from the plugin path, it imports the modules and calls the setup function."""
        path_stem = self.plugin_path.stem
        plugin_import_fmt = f"{path_stem}.{{}}"
        for module in self.plugin_path.iterdir():
            self.__attempt_load_module(module, plugin_import_fmt)

    def load(self, plugin):
        """Loads a plugin, this is used to load a plugin, it adds the plugin to the plugins dict."""
        self.plugins[getattr(plugin, "name", plugin.__class__.__name__)] = plugin

    def unload(self, plugin_name):
        """Unloads a plugin, this is used to unload a plugin, it calls the unload function of the plugin and removes it from the plugins dict."""
        if plugin_name in self.plugins:
            self.plugins[plugin_name].unload()
            del self.plugins[plugin_name]

    def unload_all(self):
        """Unloads all plugins, this is used to unload all plugins, it calls the unload function of all plugins and removes them from the plugins dict."""
        for plugin_name in self.plugins:
            self.unload(plugin_name)

    def update(self, kwargs):
        """Updates all plugins, this is used to update all plugins, it calls the update function of all plugins and passes the states to them selectively."""
        for plugin in self.plugins.values():
            params = get_func_params(plugin.update)
            plugin.update(**{k: v for k, v in kwargs.items() if k in params})

    def __attempt_load_module(self,  module, plugin_import_fmt):
        """Attempts to load a module, this is used to load a module from the plugin path, it imports the module and calls the setup function."""
        try:
            if module.is_dir():
                if (module / "__init__.py").exists():
                    self.load_module(plugin_import_fmt.format(module.name))
            elif module.suffix == ".py":
                self.load_module(plugin_import_fmt.format(module.stem))
        except Exception as e:
            print(f"Error loading module {module.name}: {e}")
