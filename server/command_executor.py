from .client_exceptions import (
    UserNotAuthenticatedException,
    CommandNotFoundException,
    ClientException,
)
from .commands import BaseCommand
from .command_handlers import BaseCommandHandler
from logging import Logger
from typing import Tuple, Dict


# todo: add logging
class CommandExecutor:
    def __init__(
        self,
        logger: Logger,
        command_handlers: Dict[str, Tuple[bool, BaseCommandHandler]],
    ):
        """
        Parameters:
            command_handlers: maps the name of the command class to a tuple 
                containing an instance of its handler and a flag for if the user must be authenticated
        """
        self._logger = logger
        self._command_handlers = command_handlers

    def execute(self, cmd: BaseCommand):
        command_type = cmd.__class__.__name__
        if command_type not in self._command_handlers:
            raise CommandNotFoundException(
                f"Could not find command handler for {command_type}"
            )

        auth_req, handler = self._command_handlers[command_type]
        if auth_req and not cmd.context.is_authenticated():
            raise UserNotAuthenticatedException(
                f"User must be autenticated to perform: {command_type}"
            )

        try:
            self._logger.info(f"Executing {cmd}. Context: {cmd.context}")
            handler.handle(cmd)
            self._logger.info(f"Successfully executed {cmd}. Context: {cmd.context}")
        except ClientException: #TODO: certain client exceptions we might want to log
            raise
        except Exception as e:
            self._logger.error(f"Error executing {cmd} with context: {cmd.context}. Exception: {e}")
            raise Exception(f"Error executing command {cmd}")
