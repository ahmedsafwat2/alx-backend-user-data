#!/usr/bin/env python3
"""
Main file
"""

from db import DB
from user import User

my_db = DB()

user_1 = my_db.add_user("omar@test.com", "SuperHashedPwd")
print(user_1.id)

user_2 = my_db.add_user("safwat@test.com", "SuperHashedPwd1")
print(user_2.id)
