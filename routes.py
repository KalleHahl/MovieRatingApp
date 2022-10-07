 
import re
from app import app
from flask import render_template, redirect, request, session
import kayttajat
import movies
from db import db

@app.route("/")
def index():
    return render_template("etusivu.html")

@app.route("/login", methods=["get", "post"])
def  login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        if not kayttajat.login(username, password):
                return render_template("error.html", message="Käyttäjätunnus tai salasana meni väärin")
        return redirect("/library")

    

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]

        password = request.form["password1"]
        password2 = request.form["password2"]
        if password != password2:
            return render_template("error.html", message = "Salasanat eivät olleet samat")
    if not kayttajat.register(username, password):
        return render_template("error.html", message="Rekisteröinti virhe!")
    return redirect("/login")

@app.route("/logout")
def logout():
    kayttajat.logout()
    return redirect("/")

@app.route("/library", methods=["get", "post"])
def library():
    if request.method == "GET":
        user_id = session["user_id"]
        sql = """SELECT name FROM movies WHERE user_id= :user_id"""
        result = db.session.execute(sql, {"user_id":user_id})
        movies = result.fetchall()
        return render_template("kirjasto.html", movies = movies)

@app.route("/add_movie", methods=["get", "post"])
def add_movie():
    if request.method == "GET":
        return render_template("add_movie.html")
    
    if request.method == "POST":
        name = request.form["name"]
        director = request.form["director"]
        year = request.form["year"]

        if not movies.add_movie(name, director, year):
            return render_template("error.html", message="Jokin meni pieleen, yritä uudelleen")
        return redirect("/library")

@app.route("/movie/<name>")
def movie(name):
    return render_template("movie.html", movie=name)
