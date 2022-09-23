import os
from flask import request, session
from db import db

from werkzeug.security import check_password_hash, generate_password_hash


def login(username, password):
    sql = "SELECT password, id FROM users WHERE name=:name"
    registered = db.session.execute(sql, {"name":username})
    user = registered.fetchone()
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
    session["user_id"] = user[1]
    session["user_name"] = user
    session["csrf_token"] = os.urandom(16).hex()
    return  True

def register(username, password):
    hash_value = generate_password_hash(password)

    try:
        sql = """INSERT INTO users (name, password) VALUES (:name, :password)"""
        db.session.execute(sql, {"name":username, "password": hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def logout():
    del session["user_id"]
    del session["user_name"]