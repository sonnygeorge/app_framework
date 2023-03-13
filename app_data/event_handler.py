import collections
from app_data.app_logger import logger

events = collections.defaultdict(list)


def subscribe(func = None, *, event = None):
    if func is None:
        return lambda func: subscribe(func, event = event)
    logger.debug(f"Subscribed {func} to {event}")
    events[event].append(func)


def unsubscribe(func = None, *, event = None):
    if func is None:
        return lambda func: unsubscribe(func, event = event)
    logger.debug(f"Unsubscribed {func} from {event}")
    events[event].remove(func)


def update(event, *args, **kwargs):
    logger.debug(f"Updating {event} with {args} and {kwargs}")
    for func in events[event]:
        func(*args, **kwargs)
