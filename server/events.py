from dataclasses import dataclass

class BaseEvent:
    pass

@dataclass
class UserLoggedInEvent:
    username:str

@dataclass
class FriendAddedEvent:
    username:str
    friend_username:str

@dataclass
class MessageSentEvent:
    to_username:str
    from_username:str
    msg:str