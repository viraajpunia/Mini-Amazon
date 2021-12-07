from flask import current_app as app


class Review:
    def __init__(self, buyer_id, product_id, rating, review, date):
        self.buyer_id = buyer_id
        self.product_id = product_id
        self.rating = rating
        self.review = review
        self.date = date

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
    def post_test(buyer_id, product_id, rating, review, date):
        rows = app.db.execute('''
INSERT INTO Feedback 
VALUES (7,100,5,'Test rating','2021-11-14 08:19:19 AM')
''',)
        return None
