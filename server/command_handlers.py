from commands import (
    BaseCommand,
    CreateAccountCommand,
    LoginCommand,
    AddFriendCommand,
    SendMessageCommand,
    DisconectCommand
)
from exceptions import (
    UsernameAlreadyExistsException,
    InvalidUsernamePasswordException,
    InvalidUsernameException,
    UserNotLoggedInException,
)
from db import Db
from event_dispatcher import EventDispatcher
from connections_manager import ConnectionsManager
from events import UserLoggedInEvent, UserLoggedOutEvent, FriendAddedEvent, MessageSentEvent


class BaseCommandHandler:
    def handle(self, command: BaseCommand):
        pass


class CreateAccountCommandHandler(BaseCommandHandler):
    def __init__(self, db: Db):
        self.db = db

    def handle(self, command: CreateAccountCommand):
        if self.db.username_exists(command.new_username):
            raise UsernameAlreadyExistsException(
                f"username: {command.username} already taken"
            )
        else:
            self.db.create_user(command.new_username, command.new_password)


class LoginCommandHandler(BaseCommandHandler):
    def __init__(
        self,
        db: Db,
        connections_manager: ConnectionsManager,
        event_dispatcher: EventDispatcher,
    ):
        self._db = db
        self._event_dispatcher = event_dispatcher
        self._connections_manager = connections_manager

    def handle(self, command: LoginCommand):
        if not self._db.is_valid(command.cred_username, command.cred_password):
            raise InvalidUsernamePasswordException(f"Invalid username and password")
        else:
            self._connections_manager.authorize_connection(
                command.cred_username, command.context.address
            )
            self._event_dispatcher.dispatch(UserLoggedInEvent(command.cred_username))


class AddFriendCommandHandler(BaseCommandHandler):
    def __init__(self, db: Db, event_dispatcher: EventDispatcher):
        self._db = db
        self._event_dispatcher = event_dispatcher

    def handle(self, command: AddFriendCommand):

        if not self._db.username_exists(command.friend_username):
            raise InvalidUsernameException(
                f"No user with username:{command.friend_username}"
            )
        else:
            self._db.add_friend(command.context.username, command.friend_username)
            self._event_dispatcher.dispath(
                FriendAddedEvent(command.context.username, command.friend_username)
            )


class SendMessageCommandHandler(BaseCommandHandler):
    def __init__(
        self,
        db: Db,
        connections_manager: ConnectionsManager,
        event_dispatcher: EventDispatcher,
    ):
        self._db = db
        self._connections_manager = connections_manager
        self._event_dispatcher = event_dispatcher

    def handle(self, command: SendMessageCommand):
        if not self._db.username_exists(command.to_username):
            raise InvalidUsernameException(
                f"No user with username:{command.to_username}"
            )
        if not self._connections_manager.is_logged_in(command.to_username):
            raise UserNotLoggedInException(
                f"user: {command.to_username} is not logged in"
            )
        else:
            self._event_dispatcher.dispatch(
                MessageSentEvent(
                    command.to_username, command.context.username, command.msg
                )
            )


class DisconectCommandHalder:
    def __init__(
        self,
        db: Db,
        connections_manager: ConnectionsManager,
        event_dispatcher: EventDispatcher
    ):
        self._db = db
        self._connections_manager = connections_manager
        self._event_dispatcher = event_dispatcher
    
    def handle(self, command:DisconectCommand):
        username = command.context.username
        if username:
            self._connections_manager.disconnect_user(username)
            self._event_dispatcher.dispatch(
                UserLoggedOutEvent(username)
            )
        else:
            self._connections_manager.disconnect(command.context.address)
            #don't need to publish event since user is anonymous
        
