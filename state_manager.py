# enum who class name is the shelf filename, and the member names are the values keys, and the value is he fdefault value
import enum
import shelve
import threading
import pathlib
import typing


# Picklable = typing.Protocol[
#     "__getstate__",
#     "__setstate__",
# ]

class Picklable:
    __setstate__: typing.Callable[[typing.Any], None]
    __getstate__: typing.Callable[[], typing.Any]


State = typing.Tuple[str, Picklable]
States = typing.Iterable[State]


class GlobalStateEnum(enum.Enum):
    @property
    def lock(self) -> threading.Lock:
        return self.__dict__.setdefault("_lock", threading.Lock())

    @property
    def value(self) -> Picklable:
        with self.lock:
            if hasattr(self, "_cached_value"):
                return getattr(self, "_cached_value")
            with shelve.open(getattr(self.__class__, "folder_path")) as db:
                return self.__dict__.setdefault(
                        "_cached_value", db.get(self.name, self._value_)
                )

    @value.setter
    def value(self, value: Picklable):
        with self.lock and shelve.open(getattr(self.__class__, "folder_path")) as db:
            db[self.name] = value
            setattr(self, "_cached_value", value)

    def __init_subclass__(cls, folder_path: str = "states", **kwargs):
        super().__init_subclass__(**kwargs)
        path = pathlib.Path(folder_path)
        path.mkdir(parents = True, exist_ok = True)
        setattr(cls, "folder_path", str(path / cls.__name__))

    @classmethod
    def __contains__(self, item: str) -> bool:
        return item in self.__members__

    @classmethod
    def __iter__(self) -> States:
        yield from ((key, self.__members__[key].value) for key in self.__members__)


class StateManager:
    def __init__(self, temp_states=None, global_states=None):
        self.temp_states = temp_states or dict()
        if global_states is not None:
            if isinstance(global_states, dict):
                self.global_states = GlobalStateEnum("global_states", global_states)
            elif isinstance(global_states, GlobalStateEnum):
                self.global_states = global_states
            else:
                raise TypeError(
                        "global_states must be a dict or a GlobalStateEnum instance"
                )
        else:
            self.global_states = GlobalStateEnum("global_states")

    def __getattr__(self, name):
        if name in self.temp_states:
            return self.temp_states[name]
        elif name in self.global_states.__members__:  # noqa
            return self.global_states[name].value  # noqa
        else:
            raise AttributeError(f"No such attribute: {name}")

    def __setattr__(self, name, value):
        if name in ("temp_states", "global_states"):
            super().__setattr__(name, value)
        elif name in self.temp_states:
            self.temp_states[name] = value
        elif name in self.global_states.__members__:  # noqa
            self.global_states[name].value = value  # noqa
        else:
            raise AttributeError(f"No such attribute: {name}")

    def __contains__(self, item: str) -> bool:
        return item in self.temp_states or item in self.global_states.__members__  # noqa

    def __iter__(self) -> States:
        yield from self.temp_states.items()
        yield from ((key, self.global_states[key].value) for key in self.global_states.__members__)  # noqa


if __name__ == "__main__":
    states = GlobalStateEnum("states", {"a": 1, "b": 2})
    for key, value in states:
        print(key, value)
