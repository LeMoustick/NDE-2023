from datetime import timedelta
from dotenv import load_dotenv
from flask import abort,Flask,Response, redirect, url_for, render_template, request, session, send_file
from flask_wtf import CSRFProtect
from markupsafe import escape

import mariadb
import os
import random

load_dotenv()

# Creation de la constante DATABASE qui stocke la base de données
try:
    DATABASE = mariadb.connect(
        host="plesk01.ancelade.net",
        port=3306,
        user=os.getenv("DATABASE_CONNECTION_USER"),
        password=os.getenv("DATABASE_CONNECTION_PASSWORD"),
        database=os.getenv("DATABASE_CONNECTION_NAME")
    )
    # La constante POINTER permet d'intéragir avec la DATABASE
    POINTER = DATABASE.cursor()
except mariadb.Error as e:
    print(e)

APP = Flask(__name__)
APP.secret_key = os.getenv("SECRET_KEY")
CSRFProtect(APP)

@APP.route("/")
def index():
    return render_template("base.html")

# Page pour le home avec les thématiques
@APP.route("/home")
def home():
    if is_logged:
        if session["choice"] == "american":
            return render_template("home_american.html")
        elif session["choice"]=="ecolo":
            return render_template("home_ecolo.html")
        else:
            abort(403)

# Page pour les crédits
@APP.route("/credits") 
def credits():
    return render_template("credits.html")

@APP.route("/assets/images/<path>")
def get_img(path):
    return send_file("assets/images/"+path)

# Page pour le quizz
@APP.route("/quiz")
def quizz():
    if is_logged():
        POINTER.execute("SELECT * FROM Questions_Quizz WHERE 1=1")
        tab = POINTER.fetchall()
        random.shuffle(tab)
        print(tab)
        print("Hello")
        return render_template("quiz.html", tab=tab)
    else:
        return render_template("/")
    
@APP.route("/api/choice", methods=["GET", "POST"])
def choice():
    # See if POST request
    if request.method == "POST":
        # Get form parameter 'choice'
        choice = request.form.get("submit_button")
        if choice == "Je suis américain":
            session["choice"] = "american"
            POINTER.execute("INSERT INTO Statistiques (Americains, Ecolos) VALUES (1, 0);")
            return redirect(url_for("home"))
        elif choice == "Je suis mangeur de graine":
            session["choice"] = "ecolo"
            POINTER.execute("INSERT INTO Statistiques (Americains, Ecolos) VALUES (1, 0);")
            return redirect(url_for("home"))
        # If parameters modified, redirect 403
        else:
            abort(403)
    else:
        return redirect("/")


@APP.route("/api/question", methods=["GET", "POST"])
def resol_question():
    if request.method == "POST":
        # Get form parameter 'choice'
        question = request.form.get("question")
        response = request.form.get("response")
        if question in [i for i in range(0, 100)] and (response in [1, 2, 3, 4]):
            POINTER.execute(
                "SELECT Bonne_reponse FROM Questions_Quizz WHERE Id_Questions_Quizz=%s",
                (question),
            )
            result = POINTER.fetchall()
            if result[0][0] == response:
                session["result_question"] += 1
                return "-1"
            return result[0][0]
        else:
            # If parameters modified, redirect 403
            abort(403)
    else:
        if is_logged():
            return redirect("/home")
        return redirect("/quiz")


@APP.route("/api/easter-egg")
def template_easter_egg():
    session["easter-egg_n"] = True


@APP.route("/api/reset")
def reset():
    session.pop("choice")
    session.pop("result_question")
    return redirect("/")

@APP.route("/api/avis")
def suggest():
    if is_logged:
        if request.method == "POST":
            suggestion = request.form.get("avis")
            username = request.form.get("username")
            username = username.replace("\x00","")
            suggestion = suggestion.replace("\x00","")
            username = escape(username)
            suggestion = escape(suggestion)

            POINTER.execute("INSERT INTO Suggestions (Username, Suggestion) VALUES (%s, %s);",(username,suggestion))
        elif request.method == "GET":
            return redirect("suggestions.html")
    else:
        abort(403)

def is_logged():
    return "choice" in session

@APP.route("/suggestion")
def fetch_suggest():
    POINTER.execute("SELECT * FROM Suggestions WHERE 1=1")
    tab = POINTER.fetchall()
    random.shuffle(tab)
    return render_template("suggestions.html",tab=tab[:4])

if __name__ == "__main__":
    APP.run(debug=True, host="0.0.0.0", port=8080)