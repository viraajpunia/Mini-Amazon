from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, uid, first_name, mid_name, last_name,
                email, address, password):
        self.id = uid
        self.first_name = first_name
        self.mid_name = mid_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.password = password

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT uid, first_name, mid_name, last_name, email, address, password
FROM UserInfo
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][-1], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0]))

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
    def register(first_name, mid_name, last_name, email, address, password):
        try:
            rows = app.db.execute("""
INSERT INTO UserInfo(first_name, mid_name, last_name, email, address, password, balance)
VALUES(:first_name, :mid_name, :last_name, :email, :address, :password, 0)
RETURNING uid
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  first_name=first_name,
                                  mid_name=mid_name,
                                  last_name=last_name,
                                  address = address)
            uid = rows[0][0]
            return User.get(uid)
        except Exception as e:
            print(str(e))
            # likely email already in use; better error checking and
            # reporting needed
            return None

    @staticmethod
    @login.user_loader
    def get(uid):
        rows = app.db.execute("""
SELECT uid, first_name, mid_name, last_name, email, address, password
FROM UserInfo
WHERE uid = :uid
""",
                              uid=uid)
        return User(*(rows[0])) if rows else None
