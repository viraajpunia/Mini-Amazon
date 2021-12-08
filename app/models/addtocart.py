from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
from .. import login

class addtocart:
    def __init__(self, uid, product_id, seller_id, quantity):
        self.uid = uid
        self.product_id = product_id
        self.seller_id = seller_id
        self.quantity = quantity


    @staticmethod
    def addtocart(uid, product_id, seller_id, quantity):
        rows = app.db.execute("""
INSERT INTO UserCarts
VALUES (:uid, :product_id, :seller_id, :quantity
)
returning *
""",
                            uid = uid,
                            product_id = product_id,
                            seller_id = seller_id,
                            quantity = quantity
                            )
        return addtocart(*(rows[0])) if rows is not None else None