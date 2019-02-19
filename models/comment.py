from datetime import datetime
from lib.db import db


class CommentModel(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    likes = db.relationship('LikeModel', cascade='all,delete', backref='comment')

    @classmethod
    def find_by_id(cls, comment_id):
        return cls.query.filter_by(id=comment_id).first()

    def verify_comment_author(self, user_id):
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