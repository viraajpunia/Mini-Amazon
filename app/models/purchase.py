from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class Purchase:
    def __init__(self, order_id, seller_id, product_id, date, uid, num_items, fulfillment_status):
        self.order_id = order_id
        self.seller_id = seller_id
        self.product_id = product_id
        self.date = date
        self.uid = uid
        self.num_items = num_items
        self.fulfillment_status = fulfillment_status

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT order_id, seller_id, product_id, date, uid, num_items, fulfillment_status
FROM Purchases
WHERE uid = :uid
''',
                              uid=uid)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT  order_id, seller_id, product_id, date, uid, num_items, fulfillment_status
FROM Purchases
WHERE uid = :uid
AND date >= :since
ORDER BY date DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
SELECT  order_id, seller_id, product_id, date, uid, num_items, fulfillment_status
FROM Purchases
WHERE uid = :uid
ORDER BY date DESC
''',
                              uid=uid)
        return [Purchase(*row) for row in rows]

#get the sellers this uid has bought from 
    @staticmethod
    def get_sellers_by_uid(uid):
        rows = app.db.execute('''
SELECT  seller_id
FROM Purchases
WHERE uid = :uid
''',
                              uid=uid)
        return [int(row[0]) for row in rows]

