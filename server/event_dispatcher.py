from events import BaseEvent
from typing import Dict
from event_handlers import BaseEventHandler
from logging import Logger

class EventDispatcher:

    def __init__(self, logger:Logger, event_dict:Dict[str,BaseEventHandler]):
        self._logger = logger
        self._event_dict = event_dict

    def dispatch(self, event:BaseEvent):
        event_type = event.__class__.__name__
        try:
            if handler := self._event_dict.get(event_type):
                handler.handle(event)
            else:
                raise Exception(f"No handler for event type: {event_type}")
        except Exception as e:
            self._logger.error(f"Error executing event: {event}. Exceptions: {e}")
            raise Exception(f"Error executing: {event}")