from flask import current_app as app


class Sellproduct2:
    def __init__(self, seller_id, product_id, current, category, name, descrip, img_link, price, available):
        self.seller_id = seller_id
        self.product_id = product_id
        self.current = current
        self.category = category
        self.name = name
        self.descrip = descrip
        self.img_link = img_link
        self.price = price
        self.available = available
        

    @staticmethod
    def get_by_seller(sid):
        rows = app.db.execute('''
SELECT SellProducts.seller_id, SellProducts.product_id, SellProducts.current, Products.category, Products.name, Products.descrip, Products.img_link, Products.price, Products.available
FROM SellProducts, Products
WHERE SellProducts.seller_id = :seller_id
AND SellProducts.current = :current
AND Products.product_id = SellProducts.product_id
''',
                              seller_id=sid,
                              current=True)
        
        return [Sellproduct2(*row) for row in rows]


    @staticmethod
    def get_by_seller_past(sid):
        rows = app.db.execute('''
SELECT SellProducts.seller_id, SellProducts.product_id, SellProducts.current, Products.category, Products.name, Products.descrip, Products.img_link, Products.price, Products.available
FROM SellProducts, Products
WHERE SellProducts.seller_id = :seller_id
AND SellProducts.current = :current
AND Products.product_id = SellProducts.product_id
''',
                              seller_id=sid,
                              current=False)
        
        return [Sellproduct2(*row) for row in rows]