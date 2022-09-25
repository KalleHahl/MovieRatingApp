 
import re
from app import app
from flask import render_template, redirect, request
import kayttajat

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
        print("moi")
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
        return render_template("error_html", message="Rekisteröinti virhe!")
    return redirect("/login")

@app.route("/logout")
def logout():
    kayttajat.logout()
    return redirect("/")

@app.route("/library", methods=["get", "post"])
def library():
    if request.method == "GET":
        return render_template("kirjasto.html")