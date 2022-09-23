import os
from flask import request, session
import db

from werkzeug.security import check_password_hash, generate_password_hash


def login(username, password):
    sql = "SELECT password, id, role FROM users WHERE name=:name"
    user = db.db.session.execute(sql, {"name":username})
    registered = user.fetchone()
    if not registered:
        return False
    if not check_password_hash(user[0], password):
        return False
    session["user_id"] = user[1]
    session["user_name"] = user
    return  True

def register(username, password):
    hash_value = generate_password_hash(password)

    try:
        sql = """INSERT INTO users (name, password) VALUES (:name, :password)"""
        db.db.session.execute(sql, {"name":username, "password": hash_value})
        db.db.session.commit()
    except:
        return False
    return login(username, password)