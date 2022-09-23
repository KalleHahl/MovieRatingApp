from app import app
from flask import render_template, redirect, request
import kayttajat

@app.route("/", methods=["GET", "POST"])
def kirjaudu():
    return render_template("etusivu.html")

@app.route("/register", methods=["get", "post"])
def rekisteröidy():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        kayttaja = request.form["käyttäjätunnus"]

        salasana = request.form["salasana"]

    if not kayttajat.rekisteroidy(kayttaja, salasana):
        return "moi"
    return redirect("/")

app.route("/library")
def kirjasto():
    return render_template("kirjasto.html")