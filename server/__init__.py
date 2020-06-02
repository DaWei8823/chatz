from . import db
from . import commands
from . import run_server
import socket, errno
from .endpoint_config import IP, PORT

def service_already_started():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((IP,PORT))
        return False
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            return True        
    finally:
        s.close()

if not service_already_started():
    run_server.run()
