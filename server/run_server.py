from .command_executor import CommandExecutor
from .command_handlers import (
    CreateAccountCommandHandler,
    LoginCommandHandler,
    AddFriendCommandHandler,
    SendMessageCommandHandler,
    DisconnectCommandHalder,
)
from .commands import (
    CreateAccountCommand,
    LoginCommand,
    AddFriendCommand,
    SendMessageCommand,
    DisconnectCommand,
)
from .connections_manager import ConnectionsManager
from .db import Db
from . import endpoint_config
from .event_dispatcher import EventDispatcher
from .event_handlers import (
    UserLoggedInEventHandler,
    UserLoggedOutEventHandler,
    FriendAddedEventHandler,
    MessageSentEventHandler,
)
from .events import (
    UserLoggedInEvent,
    UserLoggedOutEvent,
    FriendAddedEvent,
    MessageSentEvent,
)
import logging
from .models import Address
import socket
from threading import Thread

# instantiate logger
FORMAT = "%(asctime)-15s %(message)s"
logging.basicConfig(format=FORMAT, filename="Log.txt")
logger = logging.getLogger()

def run():
# instantiate db
    db = Db()

    # instantiate connection manager
    conn_mngr = ConnectionsManager(None, None)

    # instantiate event dispatcher
    dispatcher = EventDispatcher(
        logger,
        {
            UserLoggedInEvent.__name__: UserLoggedInEventHandler(db, conn_mngr),
            UserLoggedOutEvent.__name__: UserLoggedOutEventHandler(db, conn_mngr),
            FriendAddedEvent.__name__: FriendAddedEventHandler(db, conn_mngr),
            MessageSentEvent.__name__: MessageSentEventHandler(db, conn_mngr),
        },
    )

    # instantiate command executor
    executor = CommandExecutor(
        logger,
        {
            CreateAccountCommand.__name__: CreateAccountCommandHandler(db),
            LoginCommand.__name__: LoginCommandHandler(db, conn_mngr, dispatcher),
            AddFriendCommand.__name__: AddFriendCommandHandler(db, dispatcher),
            SendMessageCommand.__name__: SendMessageCommandHandler(
                db, conn_mngr, dispatcher
            ),
            DisconnectCommand.__name__: DisconnectCommandHalder(db, conn_mngr, dispatcher),
        },
    )


    # inject command executor and event_dispatcher into connection manager
    conn_mngr._command_executor = executor
    conn_mngr._event_dispatcher = dispatcher


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((endpoint_config.IP, endpoint_config.PORT))

    server_socket.listen()

    conn_mngr_thread = Thread(target=conn_mngr.start_listen)
    conn_mngr_thread.start()

    while True:
        conn, addr = server_socket.accept()
        server, port = addr
        conn_mngr.add_connection(Address(server, port), conn)