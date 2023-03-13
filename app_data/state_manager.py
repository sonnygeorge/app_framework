import shelve
import threading
from app_data.app_logger import logger


class State:
    states = dict()

    def __init__(self, defualt_value = None, store_to_disk = False, shelf_path = "states"):
        logger.debug(
                f"Creating State {self.__class__.__name__}({defualt_value!r}, {store_to_disk!r}, {shelf_path!r})"
        )
        self._value = defualt_value
        self._store_to_disk = store_to_disk
        self._shelf_path = shelf_path
        self._lock = threading.Lock()
        self._cached_value = None

    def __set_name__(self, owner, name):
        self.name = f"{getattr(owner, 'name', owner.__name__)}_{name}"
        self.states[self.name] = self

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self._cached_value is None:
            if self._store_to_disk:
                with shelve.open(self._shelf_path) as shelf:
                    self._cached_value = shelf.get(self.name, self._value)
            else:
                self._cached_value = self._value
        return self._cached_value

    def __set__(self, instance, value):
        if self._store_to_disk:
            with shelve.open(self._shelf_path) as shelf:
                shelf[self.name] = value
        self._cached_value = value

    @classmethod
    def get_states(cls):
        return {
                state.name: state._cached_value if state._cached_value is not None else state._value
                for state in cls.states.values()
        }


if __name__ == "__main__":
    class States:
        state1 = State()
        state2 = State(2)
        state3 = State(3, True)
