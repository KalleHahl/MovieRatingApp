 
import re
from app import app
from flask import render_template, redirect, request
import kayttajat

@app.route("/")
def index():
    return render_template("etusivu.html")

@app.route("/login", methods=["post"])
def  login():
    username = request.form["username"]
    password = request.form["password"]
    return redirect("/")

    

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]

        password = request.form["password1"]

    if not kayttajat.register(username, password):
        return "moi"
    return redirect("/")

app.route("/logout")
def logout():
    kayttajat.logout()
    return redirect("/")

app.route("/library")
def library():
    return render_template("kirjasto.html")