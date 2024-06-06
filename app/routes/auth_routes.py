import datetime
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app import db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    request_body = request.get_json()

    if not {"username", "email", "password"} <= request_body.keys():
        return make_response({"details": "Invalid request; missing required field"}, 400)

    username, email, password = request_body.get('username'), request_body.get('email'), request_body.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"message": f"Username {username} already exists"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": f"Email {email} already exists"}), 400

    new_user = User(username=username, email=email, created_at=datetime.now())
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    request_body = request.get_json()
    username, password = request_body.get('username'), request_body.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 402

    access_token = create_access_token(identity=user.id)

    return jsonify({"message": "Login successful", "access_token": access_token}, 200)
