from flask import current_app as app


class Sellproduct:
    def __init__(self, seller_id, product_id, seller_first_name, seller_mid_name, seller_last_name):
        self.seller_id = seller_id
        self.product_id = product_id
        self.seller_first_name = seller_first_name
        self.seller_mid_name = seller_mid_name
        self.seller_last_name = seller_last_name


    @staticmethod
    def get_by_product(pid):
        rows = app.db.execute('''
SELECT SellProducts.seller_id, SellProducts.product_id, UserInfo.first_name, UserInfo.mid_name, UserInfo.last_name
FROM SellProducts, UserInfo
WHERE product_id = :product_id
AND uid = SellProducts.seller_id
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
FROM SellProducts, UserInfo
WHERE seller_id = :seller_id
''',
                              seller_id=sid)
        return [Sellproduct(*row) for row in rows]


