import json
from ..commands import BaseCommand
from ..settings import HEADER_LENGTH, FORMAT
import socket
from ..endpoint_config import IP, PORT
from .event_parser import EventParser

class TestClient:
    
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._socket.connect((IP,PORT))
        self._event_parser = EventParser()
    
    def send_command(self, command:BaseCommand):
        serialized = serialize_command(command)
        self._socket.send(serialized)
    
    def recieve_event(self):
        msg_header = self._socket.recv(HEADER_LENGTH)
        event_type, length = msg_header.decode(FORMAT).split(" ", 1)
            
        msg_content = self._socket.recv(int(length))
        json = msg_content.decode(FORMAT)
        return self._event_parser.parse(event_type, json)



def serialize_command(command:BaseCommand):
    cmd_type = command.__class__.__name__
    cmd_encoded = json.dumps(command.__dict__).encode(FORMAT)
    
    length = len(cmd_encoded)
    header = f"{cmd_type} {length}"
    header_padded = f"{header:<{HEADER_LENGTH}}".encode(FORMAT)
    
    return header_padded + cmd_encoded