class BaseException(Exception):
   status_code = 500


class UsernameAlreadyExistsException(BaseException):
   status_code = 400

class InvalidUsernamePasswordException(BaseException):
   status_code = 400

class InvalidUsernameException(BaseException):
   status_code = 400

class UserNotLoggedInException(BaseException):
   status_code = 400