from .commands import BaseCommand
from dataclasses import dataclass


class BaseEvent:
    pass


@dataclass
class UserLoggedInEvent:
    username: str

    def __repr__(self):
        return f"UserLoggedInEvent, username: {self.username}"


@dataclass
class UserLoggedOutEvent:
    username: str

    def __repr__(self):
        return f"UserLoggedOutEvent, username: {self.username}"


@dataclass
class FriendAddedEvent:
    username: str
    friend_username: str

    def __repr__(self):
        return f"FriendAddedEvent, username: {self.username}. friend_username: {self.friend_username}"


@dataclass
class MessageSentEvent:
    to_username: str
    from_username: str
    msg: str

    def __repr__(self):
        return f"MessageSentEvent, from: {self.from_username}. to: {self.to_username}"

@dataclass
class ExceptionThrownEvent:
    msg:str
    exception_type:str

    def __repr__(self):
        return f"{self.msg}"