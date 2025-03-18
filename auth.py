from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from datetime import timedelta
import logging
auth = Blueprint('auth', __name__)

# إعداد Flask Bcrypt للتشفير
bcrypt = Bcrypt()
jwt = None  # سيتم تهيئته لاحقًا في ملف التطبيق الرئيسي

# بيانات المستخدمين التجريبية (يتم استبدالها لاحقًا بقاعدة بيانات)
users = {
    "patient": bcrypt.generate_password_hash("password123").decode('utf-8'),
    "doctor": bcrypt.generate_password_hash("doctorPass").decode('utf-8'),
    "admin": bcrypt.generate_password_hash("adminPass").decode('utf-8')
}

# تسجيل الدخول وإصدار توكن JWT
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in users and bcrypt.check_password_hash(users[username], password):
        access_token = create_access_token(identity=username, expires_delta=timedelta(hours=1))
        return jsonify({"token": access_token}), 200

    return jsonify({"msg": "Invalid credentials"}), 401

# حماية مسار خاص بالمستخدمين المسجلين
@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"msg": f"Welcome {current_user}!"}), 200


# إعداد نظام تسجيل الدخول والخروج
logging.basicConfig(filename="auth.log", level=logging.INFO, format="%(asctime)s - %(message)s")

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in users and bcrypt.check_password_hash(users[username], password):
        access_token = create_access_token(identity=username, expires_delta=timedelta(hours=1))
        logging.info(f"User {username} logged in successfully.")
        return jsonify({"token": access_token}), 200

    logging.warning(f"Failed login attempt for {username}.")
    return jsonify({"msg": "Invalid credentials"}), 401
