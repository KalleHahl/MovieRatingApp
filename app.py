from flask  import Flask
from flask import render_template
from os import getenv

app = Flask(__name__)

@app.route("/", methods=["POST"])
def kirjaudu():
    return render_template("etusivu.html")

@app.route("/register")
def rekisteröidy():
    return render_template("register.html")
