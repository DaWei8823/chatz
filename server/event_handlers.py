from events import UserLoggedInEvent
from db import Db
from connections_manager import ConnectionsManager


class UserLoggedInEventHandler:
    def __init__(self, db: Db, connections_manager: ConnectionsManager):
        self._db = db
        self._connections_manager = connections_manager

    def handle(self, event: UserLoggedInEvent):
        friends = self._db.get_friends(event.username)
        for friend in friends:
            self._connections_manager.send(friend, UserLoggedInEvent.__name__, event)
