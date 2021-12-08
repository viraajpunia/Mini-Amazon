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