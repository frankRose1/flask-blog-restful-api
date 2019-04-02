import datetime
from lib.db import db


class PostModel(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(500), nullable=True)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('CommentModel', cascade="all,delete", backref='post')

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def page(cls, page_num, per_page):
        return cls.query.paginate(page_num, per_page, False)

    @classmethod
    def find_by_category(cls, category):
        return cls.query.filter_by(category=category)

    def verify_post_author(self, user_id):
        if user_id == self.author_id:
            return True
        else:
            return False

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
