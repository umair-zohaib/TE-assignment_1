import jwt
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from flask import current_app

from app import db, ma


class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    bcrypt = Bcrypt()

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = self.bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        response = self.bcrypt.check_password_hash(self.password, password)
        return response

    @staticmethod
    def generate_jwt_token(user_id):
        data = {
            'sub': user_id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=1)
        }

        jwt_token = jwt.encode(
            data,
            current_app.config.get('SECRET_KEY'),
            algorithm="HS256"
        )
        return jwt_token

    @staticmethod
    def decode_jwt_token(jwt_token):
        try:
            payload = jwt.decode(jwt_token, current_app.config.get('SECRET_KEY'), algorithms="HS256")
            return 1, payload['sub']
        except jwt.ExpiredSignatureError:
            return -1, "Token has been expired"
        except jwt.InvalidTokenError:
            return -1, "Invalid auth token"


class UserSchema(ma.Schema):
    class Meta:
        fields = ['user_id', 'name', 'email']


user_schema = UserSchema()
