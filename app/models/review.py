from flask import current_app as app


class Review:
    def __init__(self, buyer_id, product_id, rating, review, date):
        self.buyer_id = buyer_id
        self.product_id = product_id
        self.rating = rating
        self.review = review
        self.date = date
    
    @staticmethod
    def list_ratings(buyer_id):
        rows = app.db.execute('''
SELECT *
FROM Feedback
WHERE buyer_id =:buyer_id
ORDER BY date DESC
''',
                              buyer_id=buyer_id)
        return [Review(*row) for row in rows]

    @staticmethod
    def list_ratings_buyer_ids(buyer_id,product_id):
        rows = app.db.execute('''
SELECT buyer_id
FROM Feedback
WHERE buyer_id =:buyer_id
AND product_id =:product_id
''',
                              buyer_id=buyer_id,
                              product_id=product_id)
        return [int(row[0]) for row in rows]
        


    @staticmethod
    def post_rating(buyer_id, product_id, rating, review, date):
        rows = app.db.execute('''
INSERT INTO Feedback 
VALUES (:b_id, :p_id, :rat, :rev, :dat
)
returning *
''',
                              b_id=buyer_id,
                              p_id=product_id,
                              rat=rating,
                              rev=review,
                              dat=date)
        return Review(*(rows[0])) if rows is not None else None

    @staticmethod
    def delete_row(buyer_id):
        rows = app.db.execute('''
DELETE FROM Feedback
WHERE buyer_id =:buyer_id
returning *
''',
                              buyer_id=buyer_id)
        return None

    @staticmethod
    def delete_row_product_id(product_id):
        rows = app.db.execute('''
DELETE FROM Feedback
WHERE product_id =:product_id
returning *
''',
                              product_id=product_id)
        return None

    @staticmethod
    def update_row(buyer_id,review,new_stars):
        rows = app.db.execute('''
UPDATE Feedback
SET review =:review, rating=:new_stars
WHERE buyer_id =:buyer_id
returning *
''',
                              buyer_id=buyer_id,
                              review=review,
                              new_stars=new_stars)

        return None

    @staticmethod
    def update_row_2(buyer_id,review,new_stars,product_id):
        rows = app.db.execute('''
UPDATE Feedback
SET review =:review, rating=:new_stars
WHERE buyer_id =:buyer_id
AND product_id =:product_id
returning *
''',
                              buyer_id=buyer_id,
                              review=review,
                              new_stars=new_stars,
                              product_id=product_id)

        return None



