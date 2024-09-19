#!/usr/bin/env python3
"""
Flask app
"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()
"""app.url_map.strict_slashes = False
"""


@app.route("/", methods=['GET'], strict_slashes=False)
def home() -> str:
    """home route
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users() -> str:
    """users post route
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login() -> str:
    """login
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """logout
    """
    session_id = request.cookies.get("session_id")
    try:
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(user.id)
        return redirect(url_for("home"))
    except Exception:
        abort(403)


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile() -> str:
    """profile
    """
    session_id = request.cookies.get("session_id")
    try:
        user = AUTH.get_user_from_session_id(session_id)
        return jsonify({"email": f"{user.email}"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
