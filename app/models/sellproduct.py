from flask import current_app as app


class Sellproduct:
    def __init__(self, seller_id, product_id, first_name, mid_name, last_name):
        self.seller_id = seller_id
        self.product_id = product_id
        self.first_name = first_name
        self.mid_name = mid_name
        self.last_name = last_name 
        


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
    def get_product_simple(pid):
        rows = app.db.execute('''
SELECT seller_id, product_id
FROM SellProducts
WHERE product_id = :product_id
''',
                              product_id=pid)
        return [Sellproduct(*row) for row in rows]


    @staticmethod
    def get_by_seller(sid):
        rows = app.db.execute('''
SELECT *
FROM SellProducts
''',
                              seller_id=sid)
        
        return [Sellproduct(*row) for row in rows]

    @staticmethod
    def get_by_seller2(sid):
        rows = app.db.execute('''
SELECT *
FROM SellProducts
WHERE seller_id = seller_id
''',
                              seller_id=sid)
        return [Sellproduct(*row) for row in rows]




