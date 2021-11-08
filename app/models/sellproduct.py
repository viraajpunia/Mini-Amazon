from flask import current_app as app


class Sellproduct:
    def __init__(self, seller_id, product_id):
        self.seller_id = seller_id
        self.product_id = product_id


    @staticmethod
    def get_by_product(pid):
        rows = app.db.execute('''
SELECT seller_id, product_id
FROM SellProducts
WHERE product_id = :product_id
''',
                              product_id=pid)
        return [Sellproduct(*row) for row in rows]


    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT seller_id, product_id
FROM SellProducts
''')
        return [Sellproduct(*row) for row in rows]


    @staticmethod
    def get_by_seller(sid):
        rows = app.db.execute('''
SELECT seller_id, product_id
FROM SellProducts
WHERE seller_id = :seller_id
''',
                              seller_id=sid)
        return [Sellproduct(*row) for row in rows]