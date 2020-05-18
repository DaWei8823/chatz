from events import UserLoggedInEvent, UserLoggedOutEvent, FriendAddedEvent, MessageSentEvent
from db import Db
from connections_manager import ConnectionsManager


class UserLoggedInEventHandler:
    def __init__(self, db: Db, connections_manager: ConnectionsManager):
        self._db = db
        self._connections_manager = connections_manager

    def handle(self, event: UserLoggedInEvent):
        friends = self._db.get_friends(event.username)

        for friend in friends:
            if self._connections_manager.is_logged_in(friend):
                self._connections_manager.send(
                    friend, UserLoggedInEvent.__name__, event
                )


class UserLoggedOutEventHandler:
    def __init__(self, db: Db, connections_manager):
        self._db = db
        self._connections_manager = connections_manager
    
    def handle(self, event: UserLoggedOutEvent):
        friends = self._db.get_friends(event.username)

        for friend in friends:
            if self._connections_manager.is_logged_in(friend):
                self._connections_manager.send(
                    friend, UserLoggedOutEvent.__name__, event
                )


class FriendAddedEventHandler:
    def __init__(self, db: Db, connections_manager: ConnectionsManager):
        self._db = db
        self._connections_manager = connections_manager

    def handle(self, event: FriendAddedEvent):
        if self._connections_manager.is_logged_in(event.friend_username):
            self._connections_manager.send(
                event.username, UserLoggedInEvent(event.friend_username)
            )


class MessageSentEventHandler:
    def __init__(self, db: Db, connections_manager: ConnectionsManager):
        self._db = db
        self._connections_manager = connections_manager

    def handle(self, event: MessageSentEvent):
        self._connections_manager.send(event.to_username, event)