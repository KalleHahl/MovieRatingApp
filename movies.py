import os
from flask import request, session
from db import db


def add_movie(name, director, year):
    try:
        user = session["user_id"]
        sql = """INSERT INTO movies (name, director, year, user_id) VALUES (:name, :director, :year, :user_id)"""
        db.session.execute(sql, {"name":name, "director": director, "year": year, "user_id": user})
        db.session.commit()
    except:
        return False
    return True

def review(movie, rating, text):
    user = session["user_id"]
    movie_name = movie
    try:
        sql = """INSERT INTO ratings (movie_name, user_id, rating, text) VALUES (:movie_name, :user_id, :rating, :text)"""
        db.session.execute(sql, {"movie_name":movie_name, "user_id":user, "rating":rating, "text":text})
        db.session.commit()
    except:
        return False
    return True