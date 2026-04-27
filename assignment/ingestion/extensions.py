from functools import wraps
from celery import Celery
from flask import jsonify, request, current_app
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

celery = Celery()
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def token_required(f):
    """
    Decorator to require token authentication via Authorization header.
    NOTE:
        * Expected header would be `Authorization: Bearer <token>`
        * In production, would implement a more robust auth mechanism (e.g. JWT, OAuth) and secure token storage
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization")

        if auth_header:
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({"error": "Invalid authorization header format"}), 401

        if not token:
            return jsonify({"error": "Missing authorization token"}), 401

        app_token = current_app.config.get("AUTH_TOKEN")
        if not app_token:
            return jsonify({"error": "Authentication not configured"}), 500

        if token != app_token:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated_function
