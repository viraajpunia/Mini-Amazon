from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, uid, first_name, mid_name, last_name,
                email, address, password, balance):
        self.id = uid
        self.first_name = first_name
        self.mid_name = mid_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.password = password
        self.balance = balance

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT uid, first_name, mid_name, last_name, email, address, password, balance
FROM UserInfo
WHERE email = :email
AND password = :password
""",
                              email=email,
                              password=password)
        if not rows:  # email not found
            return None
        #elif not check_password_hash(rows[0][-1], password):
            # incorrect password
            #return None
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
    def is_seller(uid):
        rows = app.db.execute("""
SELECT uid
FROM Seller
WHERE uid = :uid
""",
                              uid=uid)
        return uid in rows

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
SELECT uid, first_name, mid_name, last_name, email, address, password, balance
FROM UserInfo
WHERE uid = :uid
""",
                              uid=uid)
        return User(*(rows[0])) if rows else None


    @staticmethod
    def updatefirstname(uid, first_name):
        rows = app.db.execute('''
UPDATE UserInfo
SET first_name =:first_name
WHERE uid =:uid
returning *
''',
                              uid=uid,
                              first_name=first_name)


        return None


    @staticmethod
    def updatemiddlename(uid, mid_name):
        rows = app.db.execute('''
UPDATE UserInfo
SET mid_name =:mid_name
WHERE uid =:uid
returning *
''',
                              uid=uid,
                              mid_name=mid_name)


        return None


    @staticmethod
    def updatelastname(uid, last_name):
        rows = app.db.execute('''
UPDATE UserInfo
SET last_name =:last_name
WHERE uid =:uid
returning *
''',
                              uid=uid,
                              last_name=last_name)


        return None

    @staticmethod
    def updateemail(uid, email):
        rows = app.db.execute('''
UPDATE UserInfo
SET email =:email
WHERE uid =:uid
returning *
''',
                              uid=uid,
                              email=email)


        return None

    @staticmethod
    def updateaddress(uid, address):
        rows = app.db.execute('''
UPDATE UserInfo
SET address =:address
WHERE uid =:uid
returning *
''',
                              uid=uid,
                              address=address)


        return None

    
    @staticmethod
    def updatebalance(uid, balance):
        rows = app.db.execute('''
UPDATE UserInfo
SET balance =:balance
WHERE uid =:uid
AND balance >= :balance
returning *
''',
                              uid=uid,
                              balance=balance)


        return None

    @staticmethod
    def updatepassword(uid, password):
        rows = app.db.execute('''
UPDATE UserInfo
SET password =:password
WHERE uid =:uid
returning *
''',
                              uid=uid,
                              password=password)


        return None
