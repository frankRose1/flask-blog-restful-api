from flask import request, url_for
from lib.db import db
from lib.mailer import Mailer
from models.like import LikeModel
from argon2 import PasswordHasher

password_hasher = PasswordHasher()


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=True, unique=True)
    name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    posts = db.relationship('PostModel', cascade='all,delete', backref='author')
    comments = db.relationship('CommentModel', cascade='all,delete', backref='author')
    likes = db.relationship('LikeModel', cascade='all,delete', backref='user')
    activated = db.Column(db.Boolean, default=False)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def set_password(cls, password):
        return password_hasher.hash(password)
    
    def send_confirmation_email(self):
        link = request.url_root[:-1] + url_for('resources.users.activate_account', user_id=self.id)
        subject = 'Account Confirmation'
        text = f"Please click the link to register: {link}"
        html = f'<html>Please click the link to register: <a href="{link}"> {link}</a></html>'
        return Mailer.send(self.email, subject, text, html)

    def verify_password(self, password):
        return password_hasher.verify(self.password, password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
