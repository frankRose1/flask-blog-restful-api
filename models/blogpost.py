import datetime
from db import db

# TODO will need to set up relationships
# author is a one-to-one relationship (one author per blog post)
# comments are a one to many relationship (one blog post many comments)


class BlogPost(db.Model):
    __tablename__ = 'blogposts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    content = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_category(cls, category):
        return cls.query.filter_by(category=category)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()