from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login

#class UserCart:
#    def __init__(self, uid, product_id, quantity, balance, category, name, descrip, img_link, price):
#        self.uid = uid
#        self.product_id = product_id
#        self.quantity = quantity
#        self.balance = balance
#        self.category = category
#        self.name = name
#        self.descrip = descrip
#        self.img_link = img_link
#        self.price = price


#    @staticmethod
#    def get(uid):
#        rows = app.db.execute("""
#SELECT thing1.uid, thing1.product_id, thing1.quantity, thing1.balance, Products.category, Products.name, Products.descrip, Products.img_link, Products.price FROM 
#    (SELECT UserCarts.uid, UserCarts.product_id, UserCarts.quantity, UserAcc.balance FROM UserCarts LEFT OUTER JOIN UserAcc ON UserCarts.uid = UserAcc.uid) 
#AS thing1 LEFT OUTER JOIN Products ON thing1.product_id = Products.product_id
#""",
#                              uid=uid)
#        return [UserCart(*row) for row in rows]

class UserCart:
    def __init__(self, uid, product_id, seller_id, quantity):
        self.uid = uid
        self.product_id = product_id
        self.seller_id = seller_id
        self.quantity = quantity

    @staticmethod
    def get(uid):
        rows = app.db.execute("""
        SELECT uid, product_id, seller_id, quantity
        FROM UserCarts
        WHERE uid = :uid
        """, uid = uid)
        return UserCart(*(rows[0])) if rows else None