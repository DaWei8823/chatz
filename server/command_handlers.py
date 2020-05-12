from commands import BaseCommand, CreateAccountCommand, LoginCommand
from exceptions import (
    UsernameAlreadyExistsException,
    InvalidUsernamePasswordException,
    InvalidUsernameException,
)
from db import Db
from event_dispatcher import EventDispatcher
from connections_manager import ConnectionsManager
from events import UserLoggedInEvent


class BaseCommandHandler:
    def handle(self, command: BaseCommand):
        pass


class CreateAccountCommandHandler(BaseCommandHandler):
    def __init__(self, db: Db):
        self.db = db

    def handle(self, command: CreateAccountCommand):
        if self.db.username_exists(command.username):
            raise UsernameAlreadyExistsException(
                f"username: {command.username} already taken"
            )
        else:
            self.db.create_user(command.username, command.password)


class LoginCommandHandler(BaseCommandHandler):
    def __init__(
        self, db: Db,
        connections_manager: ConnectionsManager,
        event_dispatcher: EventDispatcher,
    ):
        self._db = db
        self._event_dispatcher = event_dispatcher
        self._connections_manager = connections_manager

    def handle(self, command: LoginCommand):
        if not self._db.is_valid(command.username, command.password):
            raise InvalidUsernamePasswordException(f"Invalid username and password")
        else:
            self._connections_manager.authorize_connection(
                command.username, command.address
            )
            self._event_dispatcher.dispatch(UserLoggedInEvent(command.username))
