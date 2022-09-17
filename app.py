from flask  import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def kirjaudu():
    return render_template("etusivu.html")

@app.route("/register")
def rekisteröidy():
    return render_template("register.html")
