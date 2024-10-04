from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User

auth_bp = Blueprint('auth', __name__)
jwt = JWTManager()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first():
        return jsonify({ "msg": "User already exists" }), 400
    
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({ "msg": "User registered successfully." }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    
    return jsonify({ "msg": "Invalid username or password." }), 401

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    data = request.get_json()
    new_password = data.get('new_password')
    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    
    if current_user:
        current_user.set_password(new_password)
        db.session.commit()
        return jsonify({ "msg": "Password updated successfully." }), 200
    
    return jsonify({ "msg": "User not found" })

@auth_bp.route('/delete-account', methods=['DELETE'])
@jwt_required()
def delete_account():
    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    
    if current_user:
        db.session.delete(current_user)
        db.session.commit()
        return jsonify({ "msg": "Account deleted successfully." }), 200
    
    return jsonify({ "msg": "User not found" }), 404