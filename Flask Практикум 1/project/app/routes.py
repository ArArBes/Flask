from flask import render_template, request, redirect, url_for
from app import app
import re

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["POST", "GET"])
def contact():
    errors = {}
    message_sent = False
    name = email = message = ''
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        errors = validate_contact_form(name, email, message)
        if not errors:
            message_sent = True
    return render_template("contact.html",
                           message_sent=message_sent,
                           errors=errors,
                           name = name,
                           email = email,
                           message = message)

def validate_contact_form(name, email, message):
    errors = {}
    if not name:
        errors['name'] = 'Пожалуйста, введите имя'
    elif len(name) < 2:
        errors['name'] = 'Имя должно быть не менее 2 символов'

    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not email:
        errors['email'] = 'Пожалуйста, введите email'
    elif not re.match(email_pattern, email):
        errors['email'] = 'Введите корректный email'

    if not message or message.strip() == '':
        errors['message'] = 'Пожалуйста, введите сообщение'

    return errors