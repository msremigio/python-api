from flask import jsonify, abort
from passlib.hash import pbkdf2_sha256
from app.extensions import db
from app.models.users import UsersModel

class UsersService:
    @staticmethod
    def post_user(request_data):
        user = db.session.query.fiter_by(email=request_data['email']).first()
        if user:
            return abort(400, description="An user with this e-mail has already been created.")
        new_user = UsersModel(request_data['email'], pbkdf2_sha256.hash(request_data['password']))
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return abort(500, description=f"{e}")
        return jsonify(new_user.to_dict())