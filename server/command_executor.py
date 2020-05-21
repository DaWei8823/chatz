from command import BaseCommand
from command_handlers import BaseCommandHandler
from typing import Tuple, Dict


#todo: add logging
class CommandExecutor:

    def __init__(self, command_handlers:Dict[str,Tuple[bool,BaseCommandHandler]]):
        """
        Parameters:
            command_handlers: maps the name of the command class to a tuple 
                containing an instance of its handler and a flag for if the user must be authenticated
        """
        self._command_handlers = command_handlers
    
    def execute(self, cmd:BaseCommand):
        if cmd.command_type in self._command_handlers:
            auth_req, handler = self._command_handlers[cmd.command_type]
            if auth_req and not cmd.context.is_authenticated():
                raise UserNotAuthenticatedException(f"User must be autenticated to perform: {cmd.command_type}")
            handler.execute(cmd)
        else:
            raise 

