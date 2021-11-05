from flask import current_app as app


class Product:
    def __init__(self, id, category, name, price, available):
        self.id = id
        self.category = category
        self.name = name
        self.price = price
        self.available = available

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT product_id, category, name, price, available
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT product_id, category, name, price, available
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_item(name):
        rows = app.db.execute('''
SELECT product_id, category, name, price, available
FROM Products
WHERE name = :name
''',
                              name=name)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_category(name):
        rows = app.db.execute('''
SELECT product_id, category, name, price, available
FROM Products
WHERE name = :category
''',
                              name=name)
        return [Product(*row) for row in rows]
