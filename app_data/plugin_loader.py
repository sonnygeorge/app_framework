import importlib
import inspect
import pathlib
from abc import ABC
import functools
from app_data.app_logger import logger


@functools.lru_cache
def get_func_params(func):
    return inspect.signature(func).parameters


class Plugin(ABC):
    def __init__(self, app, name = None):
        self.app = app
        self.name = name
        logger.debug(f"Plugin {getattr(self, 'name', self.__class__.__name__)} initialized")

    def update(self, *args, **kwargs):
        ...

    def unload(self):
        ...


class PluginLoader:
    plugins = dict()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return getattr(cls, "instance")

    def __init__(self, plugin_path = "plugins"):
        self.plugin_path = pathlib.Path(plugin_path)
        self.plugin_path.mkdir(parents = True, exist_ok = True)

    def load_module(self,  module):
        module = importlib.import_module(module)
        plugins = module.setup()
        for plugin in plugins:
            self.load(plugin)

    def load_modules(self):
        path_stem = self.plugin_path.stem
        plugin_import_fmt = f"{path_stem}.{{}}"
        for module in self.plugin_path.iterdir():
            self.__attempt_load_module(module, plugin_import_fmt)

    def load(self, plugin):
        self.plugins[getattr(plugin, "name", plugin.__class__.__name__)] = plugin

    def unload(self, plugin_name):
        if plugin_name in self.plugins:
            self.plugins[plugin_name].unload()
            del self.plugins[plugin_name]

    def unload_all(self):
        for plugin_name in self.plugins:
            self.unload(plugin_name)

    def update(self, kwargs):
        for plugin in self.plugins.values():
            params = get_func_params(plugin.update)
            plugin.update(**{k: v for k, v in kwargs.items() if k in params})

    def __attempt_load_module(self,  module, plugin_import_fmt):
        try:
            if module.is_dir():
                if (module / "__init__.py").exists():
                    self.load_module(plugin_import_fmt.format(module.name))
            elif module.suffix == ".py":
                self.load_module(plugin_import_fmt.format(module.stem))
        except Exception as e:
            print(f"Error loading module {module.name}: {e}")
