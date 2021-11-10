from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User2(UserMixin):
    def __init__(self, uid, first_name, mid_name, last_name,
                email, address, password):
        self.uid = uid
        self.first_name = first_name
        self.mid_name = mid_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.password = password
        
    @staticmethod
    def get(uid):
        rows = app.db.execute("""
SELECT uid, first_name, mid_name, last_name, email, address, password
FROM UserInfo
WHERE uid = :uid
""",
                              uid=uid)
        return User2(*(rows[0])) if rows else None

