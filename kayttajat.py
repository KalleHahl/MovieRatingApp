import os
from flask import request, session
import db

from werkzeug.security import check_password_hash, generate_password_hash


def kirjaudu(kayttaja, salasana):
    sql = "SELECT password, id, role FROM users WHERE name=:name"
    kuka = db.db.session.execute(sql, {"name":kayttaja})
    kirjautunut = kuka.fetchone()
    if not kirjautunut:
        return False
    if not check_password_hash(kayttaja[0], salasana):
        return False
    session["user_id"] = kayttaja[1]
    session["user_name"] = kayttaja
    return  True

def rekisteroidy(kayttaja, salasana):
    hash_value = generate_password_hash(salasana)

    try:
        sql = """INSERT INTO users (name, password) VALUES (:name, :password)"""
        db.db.session.execute(sql, {"name":kayttaja, "password": hash_value})
        db.db.session.commit()
    except:
        return False
    return kirjaudu(kayttaja, salasana)