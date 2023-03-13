import importlib
import inspect
import pathlib
from abc import ABC

from app_data import state_manager
import functools


@functools.lru_cache()
def _get_target_params(plugin):
    return inspect.signature(plugin.update).parameters


def _collect_args(plugins, kwargs):
    kwargs.update(
        functools.reduce(
            lambda a, b: a.update(b.send_updates()) or a,
            filter(lambda p: hasattr(p, "send_updates"), plugins.values()),
            {},
        )
    )


def _distribute_args(plugins, kwargs):
    for plugin in filter(lambda p: hasattr(p, "update"), plugins.values()):
        plugin.update(
            **{
                key: value
                for key, value in kwargs.items()
                if key in _get_target_params(plugin)
            }
        )


def _collect_and_apply_args(plugins, kwargs):
    _collect_args(plugins, kwargs)
    _distribute_args(plugins, kwargs)


class Plugin(ABC):
    def __init__(self, app, **states):
        self.app = app
        self.states = state_manager.GlobalStateEnum(self.__class__.__name__, states)

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

    def __init__(self, plugin_path="plugins"):
        self.plugin_path = pathlib.Path(plugin_path)
        self.plugin_path.mkdir(parents=True, exist_ok=True)

    def load_module(self, app, module):
        module = importlib.import_module(module)
        plugins = module.setup(app)
        for plugin in plugins:
            self.load(plugin)

    def load_modules(self, app):
        path_stem = self.plugin_path.stem
        plugin_import_fmt = f"{path_stem}.{{}}"
        for module in self.plugin_path.iterdir():
            if module.is_dir():
                if (module / "__init__.py").exists():
                    self.load_module(app, plugin_import_fmt.format(module.name))
            elif module.suffix == ".py":
                self.load_module(app, plugin_import_fmt.format(module.stem))

    def load(self, plugin):
        self.plugins[getattr(plugin, "name", plugin.__class__.__name__)] = plugin

    def unload(self, plugin_name):
        if plugin_name in self.plugins:
            self.plugins[plugin_name].unload()
            del self.plugins[plugin_name]

    def unload_all(self):
        for plugin_name in self.plugins:
            self.unload(plugin_name)

    def update(self, **kwargs):
        _collect_and_apply_args(self.plugins, kwargs)
