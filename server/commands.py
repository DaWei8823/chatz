from dataclasses import dataclass
from db import Db
from models import Address


@dataclass
class CommandContext:
    username: str
    address: Address

    def is_authenticated(self):
        return self.username is not None

    def __repr__(self):
        return f"username: {self.username}, address: {self.address}"


class BaseCommand:
    def __init__(self):
        self.context: CommandContext = None


@dataclass
class CreateAccountCommand(BaseCommand):
    new_username: str
    new_password: str

    def __repr__(self):
        return f"CreateAccount for {self.new_username}"


@dataclass
class LoginCommand(BaseCommand):
    cred_username: str
    cred_password: str

    def __repr__(self):
        return f"Login for {self.cred_username}"


@dataclass
class AddFriendCommand(BaseCommand):
    friend_username: str

    def __repr__(self):
        return f"AddFriend: {self.friend_username}"


@dataclass
class SendMessageCommand(BaseCommand):
    to_username: str
    msg: str

    def __repr__(self):
        return f"Send Message to {self.to_username}"


@dataclass
class DisconnectCommand(BaseCommand):
    pass
