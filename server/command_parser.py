from .client_exceptions import CommandNotFoundException
from . import commands
from json import loads


class CommandParser:
    def __init__(self):
        self._load_command_dict()

    def parse(self, command_type: str, json: str):
        if command_type not in self._command_dict:
            raise CommandNotFoundException(
                f"Cannot parse command type: {command_type} because it is not defined"
            )
        obj_dict = loads(json)
        return self._command_dict[command_type](**obj_dict)

    def _load_command_dict(self):
        self._command_dict = {
            attr: getattr(commands, attr)
            for attr in dir(commands)
            if attr[-7:] == "Command"
        }
