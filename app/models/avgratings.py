from flask import current_app as app


class AvgRating:
    def __init__(self, avg):
    	self.avg = avg

    @staticmethod
    def get_item_avg_rating(product_id):
        rows = app.db.execute('''
SELECT CAST(AVG(rating) AS Decimal(10,2))
FROM Feedback
WHERE product_id = :product_id
''',
                              product_id=product_id)
        return AvgRating(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_total_avg_rating():
        rows = app.db.execute('''
SELECT CAST(AVG(rating) AS Decimal(10,2))
FROM Feedback
''')
        return AvgRating(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_item_avg_rating_by_seller(product_id,seller_id):
        rows = app.db.execute('''
SELECT CAST(AVG(rating) AS Decimal(10,2))
FROM Feedback
WHERE product_id = :product_id
AND seller_id =:seller_id
''',
                              product_id=product_id,
                              seller_id = seller_id)
        return AvgRating(*(rows[0])) if rows is not None else None
