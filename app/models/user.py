from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, uid, email, first_name, last_name):
        self.uid = uid
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, uid, email, first_name, last_name
FROM UserInfo
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM UserInfo
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, first_name, last_name):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, first_name, last_name)
VALUES(:email, :password, :first_name, :last_name)
RETURNING uid
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  first_name=first_name,
                                  last_name=last_name)
            uid = rows[0][0]
            return User.get(uid)
        except Exception:
            # likely email already in use; better error checking and
            # reporting needed
            return None

    @staticmethod
    @login.user_loader
    def get(uid):
        rows = app.db.execute("""
SELECT uid, email, first_name, last_name
FROM UserInfo
WHERE uid = :uid
""",
                              uid=uid)
        return User(*(rows[0])) if rows else None
