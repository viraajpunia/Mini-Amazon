from flask import current_app as app

class Seller:
    def __init__(self, uid):
        self.uid = uid



    @staticmethod
    def get(uid):
        rows = app.db.execute("""
SELECT uid
FROM Seller
WHERE uid = :uid
""",
                              uid=uid)
        return [Seller(*row) for row in rows]

    @staticmethod
    def get_all(uid):
        rows = app.db.execute("""
SELECT uid
FROM Seller
""")
        return [Seller(*row) for row in rows]