import bcrypt
from os import environ
from os.path import isfile
import sqlite3
from typing import List

SALT_FILE_NAME = "Salt.txt"
DB_NAME = "Chatz.db"


class Db:
    def __init__(self):
        self._load_salt()
        self._conn = sqlite3.connect(DB_NAME, check_same_thread=False)

    def username_exists(self, username) -> bool:
        with self._conn as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM User WHERE Username = ?", (username,))
            return cursor.fetchone()[0] > 0

    def create_user(self, username: str, password: str) -> None:
        password_hash = bcrypt.hashpw(password.encode("utf-8"), self._db_salt)
        with self._conn as conn:
            conn.execute(
                "INSERT INTO User (Username, PasswordHash) VALUES (?,?)",
                (username, password_hash),
            )

    def is_valid(self, username: str, password: str) -> bool:
        password_hash = bcrypt.hashpw(password.encode("utf-8"), self._db_salt)
        with self._conn as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM User WHERE Username = ? AND PasswordHash = ?",
                (username, password_hash),
            )
            return cursor.fetchone() > 0

    def add_friend(self, username: str, friend_username: str):
        if username == friend_username:
            return
        with self._db() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO Friend (UserId, FriendId) 
                    SELECT u.UserId, f.UserID 
                    FROM User u 
                    INNER JOIN User f ON  f.Username = ?
                    WHERE u.Username = ? AND u.Username != f.Username
                    """,
                    (friend_username, username),
                )
            except sqlite3.IntegrityError:
                pass

    def get_friends(self, username) -> List[str]:
        with self._db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT fuser.Username 
                FROM Friend f 
                INNER JOIN User u ON f.UserId = u.UserId
                INNER JOIN User fuser ON f.FriendId = u.UserId
                WHERE u.Username =?
                """,
                (username,),
            )

            return [u[0] for u in cursor.fetchall()]

    def _load_salt(self):
        if isfile(SALT_FILE_NAME):
            with open(SALT_FILE_NAME, "rb") as salt:
                self._db_salt = salt.read()
        else:
            with open(SALT_FILE_NAME, "wb") as salt:
                self._db_salt = bcrypt.gensalt()
                salt.write(self._db_salt)

    def _db(self):
        return sqlite3.connect(DB_NAME)


def create_db():
    with sqlite3.connect(DB_NAME) as conn:

        conn.execute(
            """ 
            CREATE TABLE IF NOT EXISTS User (
                UserId INTEGER PRIMARY KEY,
                Username TEXT NOT NULL UNIQUE,
                PasswordHash TEXT NOT NULL
            )
        """
        )

        conn.execute(
            """ 
            CREATE TABLE IF NOT EXISTS Friend (
                UserId INT,
                FriendId INT,
                FOREIGN KEY (UserId) REFERENCES User(UserId),
                FOREIGN KEY (FriendId) REFERENCES User(UserId),
                PRIMARY KEY (UserId, FriendId)
            )
        """
        )
