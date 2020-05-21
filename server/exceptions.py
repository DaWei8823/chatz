class UsernameAlreadyExistsException(Exception):
   pass

class InvalidUsernamePasswordException(Exception):
   pass

class InvalidUsernameException(Exception):
   pass

class UserNotLoggedInException(Exception):
   pass

class UserNotAuthenticatedException(Exception):
   pass

class CommandNotFoundException(Exception):
   pass