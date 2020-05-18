from typing import Dict, Tuple
from socket import socket
from models import Address
import jsonpickle as jp
from settings import FORMAT
import utils

# TODO: implement forced logout if no message receieved
class ConnectionsManager:
    def __init__(self):
        self._active_connections = SocketLookup()

    def authorize_connection(self, username, address: Address):
        self._active_connections.add_user_socket(username, address)

    def send(self, username: str, event_type: str, event_obj):
        if socket := self._active_connections.get_user_socket(username):
            encoded = utils.encode_event(event_type, event_obj)
            socket.send(encoded)

    def is_logged_in(self, username):
        return self._active_connections.get_user_socket(username) is not None

    def disconect_user(self, username):
        self._active_connections.remove_user(username)
        socket = self._active_connections.get_user_socket(username)

        if socket:
            socket.close()
            socket.shutdown()
            self._active_connections.remove_user(username)

    def disconect(self, address: Address):
        if socket := self._active_connections.get_socket(address):
            socket.close()
            socket.shutdown()
            self._active_connections.remove_socket(address)


class SocketLookup:
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

    def remove_socket(self, address):
        if address in self._addr_to_socket:
            del self._address_to_username[address]
            del self._addr_to_socket[address]
