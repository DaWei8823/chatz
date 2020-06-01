from .. import events
import json

class EventParser:

    def __init__(self):
        self._load_event_dict()
    
    def parse(self, event_type, json:str):
        if event_type not in self._event_dict:
            raise ValueError(f"Can't parse event of event type {event_type}")
        
        obj_dict = json.loads(json)
        return self._event_dict[event_type](**obj_dict)   

    def _load_event_dict(self):
        self._event_dict = {
            attr : getattr(events, attr)
            for attr in dir(events)
            if attr[-5:] == "Event"
        }