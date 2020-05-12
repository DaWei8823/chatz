from typing import List

class Db:

    def username_exists(self, username) -> bool:
        pass

    def create_user(self, username:str, password:str) -> None:
        pass

    def is_valid(self, username:str, password:str) -> bool:
        pass

    def add_friend(self, username:str, friend_username:str):
        pass

    def get_friends(self, username) -> List[str]:
        pass