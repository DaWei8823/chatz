class ClientException(Exception):
   pass

class UsernameAlreadyExistsException(ClientException):
   pass

class InvalidUsernamePasswordException(ClientException):
   pass

class InvalidUsernameException(ClientException):
   pass

class UserNotLoggedInException(ClientException):
   pass

class UserNotAuthenticatedException(ClientException):
   pass

class CommandNotFoundException(ClientException):
   pass

class MalformedInputException(ClientException):
   pass