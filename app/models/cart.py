from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login

class UserCart:
    def __init__(self, uid, product_id, quantity, balance, category, name, descrip, img_link, price):
        self.uid = uid
        self.product_id = product_id
        self.quantity = quantity
        self.balance = balance
        self.category = category
        self.name = name
        self.descrip = descrip
        self.img_link = img_link
        self.price = price


    @staticmethod
    def get(uid):
        rows = app.db.execute("""
SELECT UserCarts.uid, UserCarts.product_id, UserCarts.quantity, UserInfo.balance, Products.category, Products.name, Products.descrip, Products.img_link, Products.price
FROM UserCarts, Products, UserInfo
WHERE UserCarts.uid = UserInfo.uid 
AND UserCarts.uid = :uid
AND UserCarts.product_id = Products.product_id
""",
                              uid=uid)
        return [UserCart(*row) for row in rows]



