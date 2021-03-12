from app.db import db

class Issue(db.Model):
    __tablename__ = 'issues'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))
    category_id = db.Column(db.Integer)
    status_id = db.Column(db.Integer)

    def __init__(self, email, description, category_id, status_id):
        self.email = email
        self.description = description
        self.category_id = category_id
        self.status_id = status_id


    @classmethod
    def all(cls):
        return Issue.query.all()

    @classmethod
    def create(cls, data):
        newIssue = Issue(data["email"], data["description"], data["category_id"], data["status_id"])
        db.session.add(newIssue)
        db.session.commit()
        return True

# ESTA ES LA FORMA SIN SQLALCHEMY
# class Issue(object):
#     @classmethod
#     def all(cls, conn):
#         sql = "SELECT * FROM issues"

#         cursor = conn.cursor()
#         cursor.execute(sql)

#         return cursor.fetchall()

#     @classmethod
#     def create(cls, conn, data):
#         sql = """
#             INSERT INTO issues (email, description, category_id, status_id)
#             VALUES (%s, %s, %s, %s)
#         """

#         cursor = conn.cursor()
#         cursor.execute(sql, list(data.values()))
#         conn.commit()

#         return True
