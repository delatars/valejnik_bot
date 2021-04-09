from time import time
from typing import Dict, Optional


class BannedUser:

    def __init__(self, username, ban_time, reason):
        self.username = username
        self.ban_time = ban_time
        self.reason = reason
        self.ban_timestamp = time()

    @property
    def remaining_time(self) -> int:
        elapsed = round((time() - self.ban_timestamp) // 60)

        if elapsed < self.ban_time:
            remaining = self.ban_time - elapsed
            return remaining

        return 0

    @property
    def is_banned(self):
        return True if self.remaining_time != 0 else False


class BanService:
    DEFAULT_BAN_TIME = 60 * 60  # 1 hour
    _USERS: Dict[str, BannedUser] = {}

    @classmethod
    def get_user(cls, username: str) -> Optional[BannedUser]:
        banned_user = cls._USERS.get(username)

        if banned_user is None:
            return None

        if banned_user.remaining_time == 0:
            del cls._USERS[username]

        return banned_user

    @classmethod
    def ban_user(cls, username: str, reason: str, ban_time: int = DEFAULT_BAN_TIME) -> None:
        banned_user = BannedUser(username, ban_time, reason)
        cls._USERS[banned_user.username] = banned_user

    @classmethod
    def unban_user(cls, username: str) -> None:
        try:
            del cls._USERS[username]
        except KeyError:
            pass

    @classmethod
    def user_is_banned(cls, username: str) -> bool:
        if username in cls._USERS:
            banned_user = cls.get_user(username)
            return banned_user.is_banned

        return False
