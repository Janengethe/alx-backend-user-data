#!/usr/bin/env python3
"""Module app"""
from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()

@app.route("/", methods=['Get'], strict_slashes=False)
def status() -> str:
    """Basic flask app"""
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """end-point to register a user"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        new_user = AUTH.register_user(email, password)
        if new_user is not None:
            return jsonify({
                "email": new_user.email,
                "message": "user created"
                })
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")