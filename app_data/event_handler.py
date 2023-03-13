import collections

events = collections.defaultdict(list)


def subscribe(func = None, *, event = None):
    if func is None:
        return lambda func: subscribe(func, event = event)
    events[event].append(func)


def unsubscribe(func = None, *, event = None):
    if func is None:
        return lambda func: unsubscribe(func, event = event)
    events[event].remove(func)


def update(event, *args, **kwargs):
    for func in events[event]:
        func(*args, **kwargs)


class EventHandler:
    """Facade class for the event handler module"""
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return getattr(cls, 'instance')

    def __init__(self, new_events = None):
        for event in new_events or []:
            events.setdefault(event, [])

    subscribe = subscribe
    unsubscribe = unsubscribe
    update = update
