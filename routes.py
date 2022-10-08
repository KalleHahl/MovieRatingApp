 
from cgi import test
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
                return render_template("error.html", message="Käyttäjätunnus tai salasana meni väärin", route="/login")
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
            return render_template("error.html", message = "Salasanat eivät olleet samat", route="/register")

        if len(password) > 100 or len(username)>100:
            return render_template("error.html", message = "Käyttäjänimi tai salasana liian pitkä (max 100)", route="/register")
            
    if not kayttajat.register(username, password):
        return render_template("error.html", message="Rekisteröinti virhe!", route="/register")
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

        if len(name) > 100:
            return render_template("error.html", message = "Liian pitkä nimi", route="/add_movie")
        
        if len(director) > 100:
            return render_template("error.html", message = "Liian pitkä nimi", route="/add_movie")
        
        if len(year) > 100:
            return render_template("error.html", message = "Liian suuri luku", route="/add_movie")
        

        if not movies.add_movie(name, director, year):
            return render_template("error.html", message="Jokin meni pieleen, yritä uudelleen", route="/add_movie")
        return redirect("/library")

@app.route("/movie/<name>")
def movie(name):
    user = session["user_id"]
    oma_sql = """SELECT rating, text FROM ratings WHERE movie_name= :movie_name AND user_id= :user_id"""
    oma_result = db.session.execute(oma_sql, {"movie_name":name, "user_id":user})
    omat_arvostelut = oma_result.fetchone()
    muut_sql = """SELECT rating, text, user_name FROM ratings WHERE movie_name= :movie_name AND user_id!= :user_id"""
    muut_result = db.session.execute(muut_sql, {"movie_name":name, "user_id":user})
    muut_arvostelut = muut_result.fetchall()
    return render_template("movie.html", movie=name, omat = omat_arvostelut, muut = muut_arvostelut)

@app.route("/rate_movie/<name>", methods=["get", "post"])
def rate_movie(name):
    if request.method == "GET":
        return render_template("rate_movie.html", movie = name)
    if request.method == "POST":
        rating = request.form["rating"]
        text = request.form["text"]

        try:
            rating = int(rating)
        except:
            return render_template("error.html", message="Arvosanan on oltava luku väliltä 1-10", route="/rate_movie/"+name)

        if rating > 10 or rating < 1:
            return render_template("error.html", message="Arvosanan on oltava luku väliltä 1-10", route="/rate_movie/"+name)
        if len(text) > 5000:
            return render_template("error.html", message="Liian pitkä arvostelu", route="/rate_movie/"+name)
        if not movies.review(name, rating,text):
            return render_template("error.html", message="Jokin meni pieleen", route="/rate_movie/"+name)
        return redirect("/movie/"+name)

