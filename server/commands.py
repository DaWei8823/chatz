from dataclasses import dataclass
from db import Db
from models import Address


@dataclass
class CommandContext:
    username: str
    address: Address

    def is_authenticated(self):
        return self.username is not None


@dataclass
class BaseCommand:
    context: CommandContext


@dataclass
class CreateAccountCommand(BaseCommand):
    new_username: str
    new_password: str


@dataclass
class LoginCommand(BaseCommand):
    cred_username: str
    cred_password: str


@dataclass
class AddFriendCommand(BaseCommand):
    friend_username: str


@dataclass
class SendMessageCommand(BaseCommand):
    to_username: str
    msg: str


@dataclass
class DisconectCommand(BaseCommand):
    pass
