from typing import Dict, Tuple
from socket import socket
from models import Address
import jsonpickle as jp
from settings import FORMAT
import select
import utils
from command import BaseCommand, CommandContext
from command_executor import CommandExecutor
import settings

class ConnectionsManager:
    def __init__(self):
        self._active_connections = _SocketLookup()
        self._command_executor = CommandExecutor()
    
    def start_listen(self):
        sockets = self._active_connections.get_socket_list()
        while True:
            read_sockets, _, exception_sockets = select.select(sockets, [], sockets)
            for socket in read_sockets:
                cmd = self._get_command(socket)
                addr = self._active_connections.get_address(socket)
                username = self._active_connections.get_username(addr)
                cmd.context = CommandContext(addr, username)
                self._command_executor.execute(cmd)
            for socket in exception_sockets:
                self.disconect_socket(socket)

    def authorize_connection(self, username, address: Address):
        self._active_connections.add_user_socket(username, address)

    def send(self, username: str, event_type: str, event_obj):
        if socket := self._active_connections.get_user_socket(username):
            encoded = utils.encode_event(event_type, event_obj)
            socket.send(encoded)

    def is_logged_in(self, username):
        return self._active_connections.get_user_socket(username) is not None

    def disconect_user(self, username):
        socket = self._active_connections.get_user_socket(username)

        if socket:
            socket.close()
            socket.shutdown()
            self._active_connections.remove_user(username)

    def disconect(self, address: Address):
        if socket := self._active_connections.get_socket(address):
            socket.close()
            socket.shutdown()
            self._active_connections.remove_address(address)

    def disconect_socket(self, socket):
        if addr := self._active_connections.get_address(socket)
            self.disconect(addr)       

    def _get_command(self, socket:socket) -> BaseCommand:
        msg_header = socket.recv(settings.HEADER_LENGTH)
        cmd_type, length = msg_header.decode(settings.FORMAT).split(' ', 1)
        msg_content = socket.recv(int(length))
        return utils.parse_command(cmd_type, msg_content.decode(settings.FORMAT))


class _SocketLookup:
    def __init__(self):
        self._addr_to_socket: Dict[Address, socket] = {}
        self._socket_to_address: Dict[socket, Address] = {}
        self._username_to_address: Dict[str, Address] = {}
        self._address_to_username: Dict[Address, str] = {}

    def add(self, address: Address, socket: socket):
        self._addr_to_socket[address] = socket
        self._socket_to_address[socket] = address

    def get_socket(self, address):
        return self._addr_to_socket[address]

    def get_address(self, socket):
        return self._socket_to_address.get(socket)

    def get_username(self, address):        
        return self._address_to_username.get(address)

    def add_user_socket(self, address, username):
        self._address_to_username[address] = username
        self._username_to_address[username] = address

    def get_user_socket(self, username):
        addr = self._username_to_address.get(username)
        if not addr:
            return None
        return self._addr_to_socket.get(addr)

    def remove_user(self, username):
        addr = self._username_to_address.get(username)
        if not addr:
            return
        del self._username_to_address[username]
        del self._address_to_username[addr]

        self.remove_socket(addr)

    def remove_address(self, address):
        if socket := self._addr_to_socket.get(address):
            del self._socket_to_address[socket]
            del self._addr_to_socket[address]
        if username := self._address_to_username.get(address):
            del self._address_to_username[address]
            del self._username_to_address[username]   
   
    def get_socket_list(self):
        return self._socket_to_address.keys()
