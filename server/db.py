from typing import List
import sqlite3
import bcrypt
from os import environ
from os.path import isfile


db_salt = None
SALT_FILE_NAME = "Salt.txt"



class Db:

    def __init__(self):
        self._load_salt()
        self._conn = sqlite3.connect("authorization.db")

    def username_exists(self, username) -> bool:
        pass

    def create_user(self, username:str, password:str) -> None:
        password_hash = bcrypt.hashpw(password.encode("utf-8"), self._db_salt)
        with self._conn:
            self._conn.execute("INSERT INTO User (Username, PasswordHash) VALUES (?,?)", (username, password_hash))

    def is_valid(self, username:str, password:str) -> bool:
        password_hash = bcrypt.hashpw(password.encode("utf-8"), self._db_salt)
        with self._conn:
            cursor = self._conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM User WHERE Username = ? AND PasswordHash = ?", (username, password_hash))
            return cursor.fetchone() > 0


    def add_friend(self, username:str, friend_username:str):
        if username == friend_username:
            return
        with self._conn as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                """INSERT INTO Friend (UserId, FriendId) 
                    SELECT u.UserId, f.UserID 
                    FROM User u 
                    INNER JOIN User f ON  f.Username = ?
                    WHERE u.Username = ? AND u.Username != f.Username
                    """, (friend_username, username))
            except sqlite3.IntegrityError:
                pass


    def get_friends(self, username) -> List[str]:
        pass

    def _load_salt(self):
        if isfile(SALT_FILE_NAME):
            with open(SALT_FILE_NAME, "rb") as salt:
                self._db_salt = salt.read()
        else:
            with open(SALT_FILE_NAME, "wb") as salt:
                self._db_salt = bcrypt.gensalt()
                salt.write(self._db_salt)


def create_db():
    with sqlite3.connect("authorization.db") as conn:
        
        conn.execute(""" 
            CREATE TABLE User (
                UserId INT PRIMARY KEY,
                Username TEXT NOT NULL UNIQUE,
                PasswordHash TEXT NOT NULL
            )
        """)

        conn.execute(""" 
            CREATE TABLE Friend (
                UserId INT,
                FriendId INT,
                FOREIGN KEY (UserId) REFERENCES User(UserId),
                FOREIGN KEY (FriendId) REFERENCES User(UserId),
                PRIMARY KEY (UserId, FriendId)
            )
        """)