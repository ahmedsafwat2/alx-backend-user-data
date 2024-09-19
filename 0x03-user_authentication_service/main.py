#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

user = auth.register_user(email, password)
reset_token = "ahmed"
user.reset_token = reset_token
print(user.id)
print(user.reset_token)
print(user.hashed_password)
auth.update_password(reset_token, "new")
print(user.id)
print(user.reset_token)
print(user.hashed_password)
