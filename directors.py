from db import db
from flask import render_template, session


def add_director(name, birth_year):
    try:
        user = session["user_id"]
        print(1)
        sql = """INSERT INTO directors (name, birth_year, user_id) VALUES (:name, :birth_year, :user_id)"""
        print(2)
        db.session.execute(sql, {"name":name, "birth_year":birth_year, "user_id":user})
        print(3)
        db.session.commit()
        print(4)
    except:
        return False
    return True

