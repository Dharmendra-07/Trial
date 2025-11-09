'/login'
'/register'

from flask import Blueprint, jsonify, request, current_app
from flask_security.utils import verify_password, hash_password
from models import User, db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Invalid input'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if not verify_password(password, user.password):
        return jsonify({'message': 'wrong password'}), 400

    return jsonify({
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'token': user.get_auth_token(),
    }), 200


@auth_bp.route('/register', methods=["POST"])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    active = True

    if not name or not email or not password or role not in ["manager", 'customer']:
        return jsonify({'message': 'Invalid inputs'}), 400

    if role == 'manager':
        active = False

    datastore = current_app.datastore

    if User.query.filter_by(email = email).first():
      return {'message': 'User already exists'}, 400

    datastore.create_user(name=name, email=email, password=hash_password(password), active=active)
    try:
        db.session.commit()
    except Exception as e:
        return jsonify({'message': str(e)}), 400

    role_obj = datastore.find_role(role)
    user = datastore.find_user(email=email)
    datastore.add_role_to_user(user, role_obj)

    try:
        db.session.commit()
    except Exception as e:
        return jsonify({'message': str(e)}), 400

    return jsonify({
        'id': user.id,
        'email': user.email,
        'name': user.name,
    }), 201