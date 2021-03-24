from flask import make_response, request, jsonify

from app.views.auth import auth_blueprint
from app.models.user import User, user_schema
from app import db
from app.validators.user import validate_register_schema


@auth_blueprint.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    status, msg = validate_register_schema(data)
    if status < 0:
        response = {
            'msg': msg
        }
        return make_response(jsonify(response)), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        try:
            user = User(name=name, email=email, password=password)

            access_token = user.generate_jwt_token(user.user_id)

            db.session.add(user)
            db.session.flush()

            user_details = user_schema.dump(user)
            response = {
                'msg': 'The user is registered successfully!',
                'access_token': access_token,
                'user_details': user_details
            }

            db.session.commit()
            return make_response(jsonify(response)), 201

        except Exception as e:
            response = {
                'msg': str(e)
            }
            return make_response(jsonify(response)), 401
    else:
        response = {
            'msg': 'User is already registered'
        }

        return make_response(jsonify(response)), 202


@auth_blueprint.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    try:
        if user and user.verify_password(password):
            access_token = user.generate_jwt_token(user.user_id)

            response = {
                    'msg': 'User has been successfully logged in',
                    'access_token': access_token
                }
            return make_response(jsonify(response)), 200

        else:
            response = {
                'msg': 'Email or password invalid. Try again'
            }
            return make_response(jsonify(response)), 404

    except Exception as e:
        response = {
            'msg': str(e)
        }
        return make_response(jsonify(response)), 500
