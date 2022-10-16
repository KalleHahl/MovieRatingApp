from db import db
from flask import render_template, session


def add_director(name, birth_year):
    try:
        user = session["user_id"]

        if in_database(name):
            sql = """SELECT id FROM directors WHERE name= :name"""
            sql_result = db.session.execute(sql, {"name":name})
            id = sql_result.fetchone()

            sql = """INSERT INTO user_directors (user_id, director_id) VALUES (:user_id, :director_id)"""
            db.session.execute(sql, {"user_id":user, "director_id":id[0]})
            db.session.commit()
        else:
            sql = """INSERT INTO directors (name, birth_year) VALUES (:name, :birth_year)"""
            db.session.execute(sql, {"name":name, "birth_year":birth_year})
            db.session.commit()
            
            sql = """SELECT id FROM directors WHERE name= :name"""
            sql_result = db.session.execute(sql, {"name":name})
            id = sql_result.fetchone()

            sql = """INSERT INTO user_directors (user_id, director_id) VALUES (:user_id, :director_id)"""
            db.session.execute(sql, {"user_id":user, "director_id":id[0]})
            db.session.commit()
    except:
        return False
    return True

def in_database(name):
    sql = """SELECT id FROM directors WHERE name= :name"""
    sql_result = db.session.execute(sql, {"name":name})
    id = sql_result.fetchone()
    
    if id:
        return True
    return False