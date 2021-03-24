from cryptography.fernet import Fernet
from functools import wraps
from flask import request, make_response, jsonify


from app.models.user import User


def encrypt(data):
    key = get_key()
    fernet_obj = Fernet(key)
    enc_data = fernet_obj.encrypt(data)
    return enc_data


def get_key():
    try:
        file = open("encrypt.key", "rb")
        key = file.read()
        file.close()
    except FileNotFoundError:
        key = Fernet.generate_key().decode()
        file = open("encrypt.key", "w")
        file.write(key)
    return key


def authorize(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'Authorization' not in request.headers:
            response = {"msg": "No authorization found in the header"}
            return make_response(jsonify(response)), 401

        try:
            authorization = request.headers['Authorization']
            token = authorization.split(" ")[1]
            status, msg = User.decode_jwt_token(token)
            if status < 0:
                response = {"msg": msg}
                return make_response(jsonify(response)), 401
            user_id = msg
        except Exception as e:
            response = {"msg": str(e)}
            return make_response(jsonify(response)), 401

        return func(user_id, *args, **kwargs)
    return decorated_function
