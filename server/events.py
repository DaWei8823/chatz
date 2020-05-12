from dataclasses import dataclass

class BaseEvent:
    pass

@dataclass
class UserLoggedInEvent:
    username:str