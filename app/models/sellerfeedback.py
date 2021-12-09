from flask import current_app as app


class SellerFeedback:
    def __init__(self, uid, seller_id, review,rating):
        self.uid = uid
        self.seller_id = seller_id
        self.review = review
        self.rating = rating

    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute('''
SELECT *
FROM SellerReviews
WHERE seller_id = :uid
ORDER BY rating DESC
''', uid = uid)
        return [SellerFeedback(*row) for row in rows]

    @staticmethod
    def post_review(uid,seller_id,review,rating):
        rows = app.db.execute('''
INSERT INTO SellerReviews (uid,seller_id,review,rating)
VALUES (:uid,:seller_id,:review,:rating)
returning *
''',
                              uid=uid,
                              seller_id=seller_id,
                              review=review,
                              rating=rating)
        return None

    @staticmethod
    def get_num_reviews(seller_id):
        rows = app.db.execute('''
SELECT COUNT(*)
FROM SellerReviews
WHERE seller_id=:seller_id
''',
                              seller_id=seller_id)
        return rows[0][0]

    @staticmethod
    def delete_record(buyer_id,seller_id):
        rows = app.db.execute('''
DELETE FROM SellerReviews
WHERE uid=:buyer_id
AND seller_id=:seller_id
returning *
''',
                              buyer_id=buyer_id,
                              seller_id=seller_id)
        return None

    @staticmethod
    def update_row(buyer_id,seller_id,review,new_stars):
        rows = app.db.execute('''
UPDATE SellerReviews
SET review =:review, rating=:new_stars
WHERE uid =:buyer_id
AND seller_id =:seller_id
returning *
''',
                              buyer_id=buyer_id,
                              seller_id=seller_id,
                              review=review,
                              new_stars=new_stars)

        return None

#Get average reviews for this seller
    @staticmethod
    def get_avg_rating(seller_id):
        rows = app.db.execute('''
    SELECT AVG(rating)
    FROM SellerReviews
    WHERE seller_id=:seller_id
    ''',
    seller_id=seller_id)

        return rows[0][0]
