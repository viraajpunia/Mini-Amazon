from flask import current_app as app


class Product:
    def __init__(self, id, category, name, descrip, img_link, price, available):
        self.id = id
        self.category = category
        self.name = name
        self.descrip = descrip
        self.img_link = img_link
        self.price = price
        self.available = available

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT product_id, category, name, descrip, img_link, price, available
FROM Products
WHERE product_id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT product_id, category, name, descrip, img_link, price, available
FROM Products
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_item(name):
        rows = app.db.execute('''
SELECT product_id, category, name, descrip, img_link, price, available
FROM Products
WHERE name = :name
''',
                              name=name)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_category(category):
        rows = app.db.execute('''
SELECT product_id, category, name, descrip, img_link, price, available
FROM Products
WHERE category = :category
''',
                              category=category)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_item_in_category(name, category):
        rows = app.db.execute('''
SELECT product_id, category, name, descrip, img_link, price, available
FROM Products
WHERE category = :category
AND name = :name
''',
                              name=name, category=category)
        return [Product(*row) for row in rows]




