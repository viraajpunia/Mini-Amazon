from flask import current_app as app


class Sellproductsimple:
    def __init__(self, seller_id, product_id, current):
        self.seller_id = seller_id
        self.product_id = product_id
        self.current = current
        

    @staticmethod
    def get_specific(sid, pid):
        rows = app.db.execute('''
SELECT seller_id, product_id, current
FROM SellProducts
WHERE seller_id = :seller_id
AND product_id = :product_id
''',
                              seller_id=sid,
                              product_id=pid)
        return [Sellproductsimple(*row) for row in rows]