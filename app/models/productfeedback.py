from flask import current_app as app


class ProductFeedback:
    def __init__(self, buyer_id, product_id, rating, review, date, buyer_first_name, buyer_mid_name, buyer_last_name):
        self.buyer_id = buyer_id
        self.product_id = product_id
        self.rating = rating
        self.review = review
        self.date = date
        self.buyer_first_name = buyer_first_name
        self.buyer_mid_name = buyer_mid_name
        self.buyer_last_name = buyer_last_name


    @staticmethod
    def get_item_reviews(product_id):
        rows = app.db.execute('''
SELECT Feedback.buyer_id, Feedback.product_id, Feedback.rating, Feedback.review, Feedback.date, UserInfo.first_name, UserInfo.mid_name, UserInfo.last_name
FROM Feedback, UserInfo
WHERE product_id = :product_id
AND uid = Feedback.buyer_id
''',
                              product_id=product_id)
        return [ProductFeedback(*row) for row in rows]


    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT Feedback.buyer_id, Feedback.product_id, Feedback.rating, Feedback.review, Feedback.date, UserInfo.first_name, UserInfo.mid_name, UserInfo.last_name
FROM Feedback, UserInfo
''')
        return [ProductFeedback(*row) for row in rows]