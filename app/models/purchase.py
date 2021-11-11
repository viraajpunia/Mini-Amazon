from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class Purchase:
    def __init__(self, order_id, seller_id, product_id, current_timestamp, uid, num_items, fulfillment_status):
        self.order_id = order_id
        self.seller_id = seller_id
        self.product_id = product_id
        self.current_timestamp = current_timestamp
        self.uid = uid
        self.num_items = num_items
        self.fulfillment_status = fulfillment_status

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT order_id, seller_id, product_id, current_timestamp, uid, num_items, fulfillment_status
FROM Purchases
WHERE uid = :uid
''',
                              uid=uid)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT  order_id, seller_id, product_id, current_timestamp, uid, num_items, fulfillment_status
FROM Purchases
WHERE uid = :uid
AND current_timestamp >= :since
ORDER BY current_timestamp DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]
