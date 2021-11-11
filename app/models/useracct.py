from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class UserAccount(UserMixin):
    def __init__(self, uid, balance):
        self.uid = uid
        self.balance = balance
        
    @staticmethod
    def get(uid):
        rows = app.db.execute("""
SELECT uid, balance
FROM UserAcc
WHERE uid = :uid
""",
                              uid=uid)
        return UserAccount(*(rows[0])) if rows else None

