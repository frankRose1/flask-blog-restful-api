from db import db
from argon2 import PasswordHasher

password_hasher = PasswordHasher()


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def set_password(cls, password):
        return password_hasher.hash(password)

    def verify_password(self, password):
        return password_hasher.verify(self.password, password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
