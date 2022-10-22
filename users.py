import os
from flask import request, session, abort
from db import db
import secrets
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
    session["user_name"] = username
    session["csrf_token"] = secrets.token_hex(16)
    return  True

def register(username, password):
    hash_value = generate_password_hash(password)

    try:
        sql = """INSERT INTO users (name, password) VALUES (:name, :password)"""
        db.session.execute(sql, {"name":username, "password": hash_value})
        db.session.commit()
    except:
        return False
    return True

def logout():
    del session["user_id"]
    del session["user_name"]

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)