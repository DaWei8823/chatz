from dataclasses import dataclass
from db import Db
from models import Address

class BaseCommand:
    pass

#Create account
#Login
#Add friend
#Send Message
#Logout

@dataclass
class CreateAccountCommand(BaseCommand):
    username:str
    password:str    


@dataclass
class LoginCommand(BaseCommand):
    username:str
    password:str
    address:Address

        


# @dataclass
# class AddFriendCommand(BaseCommand):
#     db:Db
#     username:str
#     friend_username:str

#     def exec(self):
#         self.validate()
#         self.db.add_friend(self.username, self.friend_username)

#     def validate(self):
#         if not self.db.username_exists(self.friend_username):
#             raise InvalidUsernameException(f"No user with username:{self.friend_username}")

