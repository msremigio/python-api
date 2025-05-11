from flask import jsonify, abort
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256
from app.extensions import db
from app.models.users import UsersModel

class UsersService:
    @staticmethod
    def post_user(request_data):
        user = UsersModel.query.filter_by(email=request_data['email']).first()
        if user:
            return abort(400, description="An user with this e-mail has already been created.")
        new_user = UsersModel(email=request_data['email'], password=pbkdf2_sha256.hash(request_data['password']))
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return abort(500, description=f"{e}")
        return jsonify(new_user.to_dict())
    
    @staticmethod
    def authenticate(request_data):
        user = UsersModel.query.filter_by(email=request_data['email']).first()
        if user:
            if pbkdf2_sha256.verify(request_data['password'], user.password):
                access_token = create_access_token(identity=user.id)
                return jsonify({'access_token': access_token})
        return abort(401, description="There is no existing user with the provided credentials.")