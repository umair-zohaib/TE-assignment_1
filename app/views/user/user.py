from flask import make_response, request, jsonify

from app.views.user import user_blueprint
from app.models.user import User, user_schema
from app import db
from app.validators.user import validate_update_schema
from app.utils.utils import authorize


@user_blueprint.route("/delete_user", methods=["DELETE"])
@authorize
def delete_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()

    user_details = user_schema.dump(user)
    response = {"msg": "User has been deleted", "user_details": user_details}

    db.session.delete(user)
    db.session.commit()
    return make_response(jsonify(response)), 201


@user_blueprint.route("/update_user", methods=["PUT"])
@authorize
def update_user(user_id):
    data = request.get_json()

    status, msg = validate_update_schema(data)
    if status < 0:
        response = {
            'msg': msg
        }
        return make_response(jsonify(response)), 401

    user = User.query.filter_by(user_id=user_id).first()
    for key, value in data.items():
        setattr(user, key, value)

    db.session.commit()
    user_details = user_schema.dump(user)
    response = {
        'msg': 'User has been updated successfully',
        'user_details': user_details
    }
    return make_response(jsonify(response)), 201
