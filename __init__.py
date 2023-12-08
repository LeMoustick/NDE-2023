from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, render_template, request, session

import mariadb
import os

load_dotenv()

# Creation de la constante DATABASE qui stocke la base de données
DATABASE = mariadb.connect(
    host="plesk01.ancelade.net",
    port=3306,
    user=os.getenv("DATABASE_CONNECTION_USER"),
    password=os.getenv("DATABASE_CONNECTION_PASSWORD"),
    database=os.getenv("DATABASE_CONNECTION_NAME")
)

# La constante POINTER permet d'intéragir avec la DATABASE
POINTER = DATABASE.cursor()

APP = Flask(__name__)
APP.secret_key = os.getenv("SECRET_KEY")
APP.permanent_session_lifetime = timedelta(minutes=5)

@APP.route("/")
def home():
    return render_template("index.html")

# Page pour le home avec les thématiques
@APP.route("/home") 
def home():
    return render_template("home.html")

# Page pour les crédits
@APP.route("/credits") 
def credits():
    return render_template("credits.html")

# Page pour le quizz
@APP.route("/quizz")
def quizz():
    return render_template("quizz.html")

if __name__ == "__main__":
    APP.run(debug=True, host="0.0.0.0")