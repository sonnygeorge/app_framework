import collections


class EventHandler:
    def __init__(self, events=None):
        self.events = collections.defaultdict(list)
        for event in events or []:
            self.events.setdefault(event, [])

    def subscribe(self, func = None, *, event = None):
        if func is None:
            return lambda func: self.subscribe(func, event = event)
        self.events[event].append(func)

    def unsubscribe(self, func = None, *, event = None):
        if func is None:
            return lambda func: self.unsubscribe(func, event = event)
        self.events[event].remove(func)

    def update(self, event, *args, **kwargs):
        for func in self.events[event]:
            func(*args, **kwargs)

    def __call__(self, func = None, *, event = None):
        return self.subscribe(func, event = event)
