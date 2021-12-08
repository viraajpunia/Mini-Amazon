from flask import current_app as app


class Seller:
    def __init__(self, id):
        self.id = id

@staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT uid
FROM Seller
WHERE uid = :uid
''',
                              uid=uid)
        return Seller(*(rows[0])) if rows is not None else None