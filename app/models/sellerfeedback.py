from flask import current_app as app


class SellerFeedback:
    def __init__(self, uid, review_id, review):
        self.uid = uid
        self.review_id = review_id
        self.review = review

    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute('''
SELECT *
FROM SellerReviews
WHERE uid = :uid
''', uid = uid)
        return [SellerFeedback(*row) for row in rows]

    @staticmethod
    def post_review(uid,review):
        rows = app.db.execute('''
INSERT INTO SellerReviews (uid,review_id,review)
VALUES (:uid,DEFAULT,:review)
returning *
''',
                              uid=uid,
                              review=review)
        return None

    @staticmethod
    def get_num_reviews(uid):
        rows = app.db.execute('''
SELECT COUNT(*)
FROM SellerReviews
WHERE uid=:uid
''',
                              uid=uid)
        return rows[0][0]
