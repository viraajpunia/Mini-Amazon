from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login

class UserCart(UserMixin):
    def __init__(self, uid, seller_id, product_id, balance, category, name, price):
        self.uid = uid
        self.seller_id = seller_id
        self.product_id = product_id
        self.balance = balance
        self.category = category
        self.name = name
        self.price = price




    @staticmethod
    def cart_by_user(uid):
        rows = app.db.execute("""
SELECT uid, product_id, quantity
FROM UserCarts
WHERE uid = :uid
""",
                              uid=uid)
        return [UserCarts(*row) for row in rows]