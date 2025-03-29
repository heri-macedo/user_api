import logging
from pydantic import ValidationError
from api.services.user_service import UserService
from api.schemas.user import (
    UserCreate,
    UserUpdate,
    UserListQuerySchema
)

from flask import Blueprint, jsonify, request

logger = logging.getLogger(__name__)
user_bp = Blueprint('users', __name__, url_prefix='/users')

user_service = UserService()

@user_bp.route('/', methods=['GET'])
def list_users():
    try:
        data = request.get_json(silent=True)
        if data:
            raise ValueError("Request should not have a body")

        query_params = request.args.to_dict()

        validated_query_params = UserListQuerySchema(**query_params)
        page = validated_query_params.page
        per_page = validated_query_params.per_page

        result = user_service.get_users_paginated(page, per_page)

    except ValidationError as e:
        errors = [err["msg"] for err in e.errors()]
        logger.error(f'Validation error: {errors}')
        return jsonify({'errors': errors}), 422
    except ValueError as e:
        return jsonify({"errors": str(e)}), 400
    except Exception as e:
        logger.error(f'An unexpected error occurred: {str(e)}')
        return jsonify({"errors": "An unexpected error occurred"}), 500

    return jsonify(result), 200

@user_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    try:
        data = request.get_json(silent=True)
        if data:
            raise ValueError("Request should not have a body")

        user = user_service.get_user(id)
    except ValueError as e:
        return jsonify({"errors": str(e)}), 404
    except Exception as e:
        logger.error(f'An unexpected error occurred: {str(e)}')
        return jsonify({"errors": "An unexpected error occurred"}), 500
    return jsonify(user), 200

@user_bp.route('/', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        validated_data = UserCreate(**data)
        if not data:
            return jsonify({"errors": 'No input data provided'}), 400

        user = user_service.create_user(validated_data)
        logger.info(f'User created with ID: {user.id}')

    except ValidationError as e:
        errors = [err["msg"] for err in e.errors()]
        logger.error(f'Validation error: {errors}')
        return jsonify({'errors': errors}), 422
    except ValueError as e:
        return jsonify({'errors': str(e)}), 400
    except Exception as e:
        logger.error(f'An unexpected error occurred: {str(e)}')
        return jsonify({'errors': 'An unexpected error occurred'}), 500

    return jsonify({'message': 'User created successfully'}), 201

@user_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({'errors': 'No input data provided'}), 400

        validated_data = UserUpdate(**data)
        user = user_service.update_user(id, validated_data.model_dump(exclude_unset=True))
    except ValidationError as e:
        errors = [err["msg"] for err in e.errors()]
        logger.error(f'Validation error: {errors}')
        return jsonify({'errors': errors}), 422
    except ValueError as e:
        return jsonify({'errors': str(e)}), 400
    except Exception as e:
        logger.error(f'An unexpected error occurred: {str(e)}')
        return jsonify({'errors': 'An unexpected error occurred'}), 500

    return jsonify({"message": f"User {id} updated"}), 201

@user_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        data = request.get_json(silent=True)
        if data:
            return jsonify({"errors": "Endpoint dos not expect body params"}), 400

        user_service.delete_user(id)
    except ValueError as e:
        return jsonify({"errors": str(e)}), 400
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({"errors": "An unexpected error occurred"}), 500

    return jsonify({"message": "User deleted successfully"}), 204