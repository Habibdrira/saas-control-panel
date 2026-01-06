from flask import request, jsonify, current_app
from app import db
from app.models import User
from app.api import bp


@bp.route('/users', methods=['POST'])
def create_user():
    # Vérification de la clé API
    api_key = request.headers.get('X-API-KEY')
    if api_key != current_app.config['MICROBLOG_API_KEY']:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json() or {}

    # Vérification des champs requis
    required_fields = ['username', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing fields'}), 400

    # Vérifier si l'utilisateur existe déjà
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'User already exists'}), 409

    # Création de l'utilisateur
    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201
