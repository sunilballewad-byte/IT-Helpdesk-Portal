from flask import Blueprint, render_template, request, redirect, url_for

auth = Blueprint("auth", __name__)

@auth.route("/")
def index():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login():

    email = request.form.get("email")
    password = request.form.get("password")

    print("Email:", email)
    print("Password:", password)

    return redirect(url_for("dashboard.dashboard_home"))