#!/usr/bin/env python3

"""
Session Authentication Views
"""
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User
from os import getenv
from api.v1.app import auth


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /auth_session/login
    Return:
      - Response
    """
    u_email = request.form.get("email")
    u_pwd = request.form.get("password")
    if u_email is None:
        return jsonify({"error": "email missing"}), 400
    if u_pwd is None:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": u_email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(users) <= 0:
        return jsonify({"error": "no user found for this email"}), 404
    if not users[0].is_valid_password(u_pwd):
        return jsonify({"error": "wrong password"}), 401
    session_id = auth.create_session(users[0].id)
    response = jsonify(users[0].to_json())
    response.set_cookie(getenv("SESSION_NAME"), session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """ DELETE /auth_session/logout
    Return:
      - Response
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
