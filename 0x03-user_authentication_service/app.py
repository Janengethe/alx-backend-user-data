#!/usr/bin/env python3
"""Module app"""
from flask import Flask, abort, jsonify, redirect, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def status() -> str:
    """Basic flask app"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    Login Route
    create a new session for the user, store it the session ID as a cookie
    with key "session_id" on the response and
    return a JSON payload of the form
    """
    email = request.form.get("email")
    password = request.form.get("password")
    user = AUTH.valid_login(email, password)
    if not user:
        abort(401)
    session_id = AUTH.create_session(email)
    msg = {"email": email, "message": "logged in"}
    response = jsonify(msg)
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """
    The request is expected to contain the session ID as a cookie
    with key "session_id".
    Find the user with the requested session ID.
    If the user exists destroy the session and redirect the user to GET /.
    If the user does not exist, respond with a 403 HTTP status.
    """
    s_cookie = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(s_cookie)
    if s_cookie is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
