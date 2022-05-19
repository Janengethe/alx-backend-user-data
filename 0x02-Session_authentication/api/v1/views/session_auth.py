#!/usr/bin/env python3
"""
Module session_auth
handles all routes for the Session authentication
"""
from os import getenv
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """authentication based on a Session ID stored in cookie"""
    email = request.form.get("email")
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get("password")
    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

    user = users[0]
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    SESSION_NAME = getenv("SESSION_NAME")
    response = jsonify(user.to_json())
    response.set_cookie(session_id)
    return response
