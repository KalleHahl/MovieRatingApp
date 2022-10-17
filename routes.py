 

from app import app
from flask import render_template, redirect, request, session
import kayttajat
import movies
import directors
from db import db
import datetime

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
        
        if len(password) < 8 or len(username) == 0:
            return render_template("error.html", message = "Käyttäjänimi tai salasana liian lyhyt", route="/register")


            
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

        sql = """SELECT name FROM movies JOIN user_movies ON movies.id=user_movies.movie_id WHERE user_movies.user_id= :user_id"""
        result = db.session.execute(sql, {"user_id":user_id})
        movies = result.fetchall()

        sql = """SELECT name FROM directors JOIN user_directors ON directors.id=user_directors.director_id WHERE user_directors.user_id= :user_id"""
        result = db.session.execute(sql, {"user_id":user_id})
        directors = result.fetchall()

        return render_template("kirjasto.html", movies = movies, directors=directors, username = session["user_name"])


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

    movie_sql = """SELECT director, year FROM movies WHERE name= :name"""
    movie_result = db.session.execute(movie_sql, {"name":name})
    movie_info = movie_result.fetchone()

    oma_sql = """SELECT rating, text FROM ratings WHERE movie_name= :movie_name AND user_id= :user_id"""
    oma_result = db.session.execute(oma_sql, {"movie_name":name, "user_id":user})
    omat_arvostelut = oma_result.fetchone()

    muut_sql = """SELECT rating, text, user_name FROM ratings WHERE movie_name= :movie_name AND user_id!= :user_id"""
    muut_result = db.session.execute(muut_sql, {"movie_name":name, "user_id":user})
    muut_arvostelut = muut_result.fetchall()

    sql = """SELECT Avg(rating) FROM ratings WHERE movie_name= :movie_name"""
    sql_result = db.session.execute(sql, {"movie_name":name})
    avg = sql_result.fetchone()
    if avg[0]:
        print(1)
        avg = round(avg[0], 1)
    else:
        avg = "Ei vielä arvosteluja!"

    return render_template("movie.html", movie=name, movie_info = movie_info, omat = omat_arvostelut, muut = muut_arvostelut, avg=avg)


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


@app.route("/add_director", methods=["get", "post"])
def add_director():

    if request.method == "GET":
        return render_template("add_director.html")

    if request.method == "POST":

        director = request.form["name"]
        birth_year = request.form["year"]
        now = datetime.date.today()
        now_year = now.year

        try:
            birth_year = int(birth_year)
        except:
            return render_template("error.html", message="Syntymävuoden pitää olla luku", route="/add_director")

        if len(director) > 100 or 1500 > birth_year or birth_year > now_year:
            return render_template("error.html", message="Ohjaajan nimi liian pitkä tai syntymävuosi ei ole sopiva", route="/add_director")

        if not directors.add_director(director, birth_year):
            return render_template("error.html", message="Jotain meni pieleen", route="/add_director")
        
        return redirect("/library")

@app.route("/director/<name>")
def director(name):

    sql = """SELECT DISTINCT name FROM movies WHERE director= :name"""
    sql_result = db.session.execute(sql, {"name":name})
    movies = sql_result.fetchall()

    sql = """SELECT Avg(rating) FROM ratings WHERE movie_name IN (SELECT DISTINCT name FROM movies WHERE director= :director)"""
    sql_result = db.session.execute(sql, {"director":name})
    avg = sql_result.fetchone()

    if avg[0]: 
        avg = round(avg[0], 1)
    else:
        avg = "Ei vielä arvosteluja!"

    return render_template("director.html", name=name, movies=movies, avg= avg)
        
