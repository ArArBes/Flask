from flask import render_template, request, redirect, url_for
from app import app

@app.route("/")
def home():
    return render_template("form.html")

@app.route("/submit", methods=["POST", "GET"])
def submit():
    if request.method == "POST":
        name = request.form.get("name")
        color = request.form.get("color")
        profession = request.form.get("profession")
        hobbies = request.form.getlist("hobbies")
        level = request.form.get("level")
        return render_template("result.html", name=name, color=color, profession=profession, hobbies=hobbies, level=level)
    else:
        return redirect(url_for("form"))

