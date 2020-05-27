from commands import BaseCommand
from command_handlers import BaseCommandHandler
from typing import Tuple, Dict
from client_exceptions import UserNotAuthenticatedException, CommandNotFoundException, ClientException
from logging import Logger

#todo: add logging
class CommandExecutor:

    def __init__(self, logger:Logger, command_handlers:Dict[str,Tuple[bool,BaseCommandHandler]]):
        """
        Parameters:
            command_handlers: maps the name of the command class to a tuple 
                containing an instance of its handler and a flag for if the user must be authenticated
        """
        self._logger = logger 
        self._command_handlers = command_handlers
    
    def execute(self, cmd:BaseCommand):
        if cmd.command_type not in self._command_handlers:
            raise CommandNotFoundException(f"Could not find command handler for {cmd.command_type}")
        
        auth_req, handler = self._command_handlers[cmd.command_type]        
        if auth_req and not cmd.context.is_authenticated():
            raise UserNotAuthenticatedException(f"User must be autenticated to perform: {cmd.command_type}")

        try:
            self._logger.info(f"Executing {cmd}. Context: {cmd.context}")
            handler.execute(cmd)
            self._logger.info(f"Successfully executed {cmd}. Context: {cmd.context}")
        except Exception as e:
            self._logger.error(f"Error executing {cmd} with context: {cmd.context}. Exception: {e}")
            if issubclass(e, ClientException):
                raise e
            else:
                raise Exception(f"Error executing command {cmd}")
        


