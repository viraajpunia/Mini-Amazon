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
    def get_all_sorted(available=True):
        rows = app.db.execute('''
SELECT product_id, category, name, descrip, img_link, price, available
FROM Products
ORDER BY price DESC
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_item(name):
        rows = app.db.execute('''
SELECT product_id, category, name, descrip, img_link, price, available
FROM Products
WHERE name LIKE '%' || :name || '%' OR descrip LIKE '%' || :name || '%'
''',
                              name=name)
        return [Product(*row) for row in rows]


    @staticmethod
    def get_item_sorted(name):
        rows = app.db.execute('''
SELECT product_id, category, name, descrip, img_link, price, available
FROM Products
WHERE name LIKE '%' || :name || '%' OR descrip LIKE '%' || :name || '%'
ORDER BY price DESC
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
    def get_category_sorted(category):
        rows = app.db.execute('''
SELECT product_id, category, name, descrip, img_link, price, available
FROM Products
WHERE category = :category
ORDER BY price DESC
''',
                              category=category)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_item_in_category(name, category):
        rows = app.db.execute('''
SELECT product_id, category, name, descrip, img_link, price, available
FROM Products
WHERE category = :category
AND (name LIKE '%' || :name || '%' OR descrip LIKE '%' || :name || '%')
''',
                              name=name, category=category)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_item_in_category_sorted(name, category):
        rows = app.db.execute('''
SELECT product_id, category, name, descrip, img_link, price, available
FROM Products
WHERE category = :category
AND (name LIKE '%' || :name || '%' OR descrip LIKE '%' || :name || '%')
ORDER BY price DESC
''',
                              name=name, category=category)
        return [Product(*row) for row in rows]

    @staticmethod
    def add_item(product_id, name, category, descrip, img_link, price, available = True):
        rows = app.db.execute('''
INSERT INTO Products
VALUES(:product_id, :category, :name, :descrip, :img_link, :price, :available)
returning *
''',
                              product_id=product_id,
                              name=name,
                              category=category,
                              descrip=descrip,
                              img_link=img_link,
                              price=price,
                              available=available)
        return None

    @staticmethod
    def edit_item(name, category, descrip, img_link, price):
        rows = app.db.execute('''
UPDATE Products
SET category = :category, descrip = :descrip, img_link = :img_link, price = :price
WHERE name = :name
returning *
''',
                              name=name,
                              category=category,
                              descrip=descrip,
                              img_link=img_link,
                              price=price)
        return None




