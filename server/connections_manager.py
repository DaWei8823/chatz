from typing import Dict,Tuple
from socket import socket
from models import Address
import jsonpickle as jp
from settings import FORMAT
import utils


class ConnectionsManager:

    def __init__(self):
        self._active_connections = SocketLookup()
        self._logged_in_users: Dict[str, socket] = dict()

    def authorize_connection(self, username, address:Address):
        socket = self._active_connections.get_socket(address)
        self._logged_in_users[username] = socket

    def send(self, username:str, event_type:str, event_obj):
        socket = self._logged_in_users.get(username)
        if not socket:
            return
        else:
            encoded = utils.encode_event(event_type, event_obj)
            socket.send(encoded)
        



class SocketLookup:
    def __init__(self):
        self._addr_to_socket:Dict[Address,socket] = {}
        self._socket_to_address:Dict[socket,Address] = {}
    
    def add(self, address:Address, socket:socket):
        self._addr_to_socket[address] = socket
        self._socket_to_address[socket] = address
    
    def get_socket(self, address):
        return self._addr_to_socket[address]
