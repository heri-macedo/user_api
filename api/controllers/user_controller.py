import logging

from api.services.user_service import UserService

from flask import Blueprint, jsonify, request

logger = logging.getLogger(__name__)
user_bp = Blueprint('users', __name__, url_prefix='/users')

user_service = UserService()

@user_bp.route('/', methods=['GET'])
def list_users():
    page = request.args.get('page', type=int)
    per_page = request.args.get('per_page', type=int)

    if page and per_page:
        result = user_service.get_users_paginated(page, per_page)
    else:
        result = user_service.get_users()

    return jsonify(result), 200

@user_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = user_service.get_user(id)
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f'An unexpected error occurred: {str(e)}')
        return jsonify({"error": "An unexpected error occurred"}), 500
    return jsonify(user), 200

@user_bp.route('/', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        user = user_service.create_user(data)
        logger.info(f'User created with ID: {user.id}')
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f'An unexpected error occurred: {str(e)}')
        return jsonify({'error': 'An unexpected error occurred'}), 500

    return jsonify({'message': 'User created successfully'}), 201

@user_bp.route('/<int:id>', methods=['PUT'])
def update_user(user_id):
    result, status = user_service.update_user(user_id)
    return jsonify(result), status

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result, status = user_service.delete_user(user_id)
    return jsonify(result), status