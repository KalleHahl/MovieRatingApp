import os
from flask import request, session
from db import db


def add_movie(name, director, year):
    try:
        user = session["user_id"]

        if in_database(name):
            sql = """SELECT movie_id FROM movies WHERE name= :name"""
            sql_result = db.session.execute(sql, {"name": name})
            movie_id = sql_result.fetchone()

            sql = """INSERT INTO user_movies (user_id, movie_id) VALUES (:user_id, :movie_id)"""
            db.session.execute(sql, {"user_id": user, "movie_id":movie_id})
            db.session.commit()
            
        else:
            sql = """INSERT INTO movies (name, director, year) VALUES (:name, :director, :year)"""
            db.session.execute(sql, {"name":name, "director": director, "year": year})
            db.session.commit()

            sql = """SELECT movie_id FROM movies WHERE name= :name"""
            sql_result = db.session.execute(sql, {"name": name})
            movie_id = sql_result.fetchone()

            sql = """INSERT INTO user_movies (user_id, movie_id) VALUES (:user_id, :movie_id)"""
            db.session.execute(sql, {"user_id": user, "movie_id":movie_id})
            db.session.commit()

    except:
        return False
    return True

def review(movie, rating, text):
    user = session["user_id"]
    username = session["user_name"]
    movie_name = movie
    try:
        sql = """INSERT INTO ratings (movie_name, user_id, rating, text, user_name) VALUES (:movie_name, :user_id, :rating, :text, :user_name)"""
        db.session.execute(sql, {"movie_name":movie_name, "user_id":user, "rating":rating, "text":text, "user_name":username})
        db.session.commit()
    except:
        return False
    return True

def in_database(name):
    sql = """SELECT movie_id FROM movies WHERE name= :name"""
    sql_result = db.session.execute(sql, {"name": name})
    movie_id = sql_result.fetchone()

    if movie_id:
        return True
    return False
