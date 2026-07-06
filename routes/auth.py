from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash

from models import User

auth = Blueprint("auth", __name__)


# Login Page
@auth.route("/")
def index():
    return render_template("login.html")


# Login Process
@auth.route("/login", methods=["POST"])
def login():

    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        flash("Please enter email and password.", "danger")
        return redirect(url_for("auth.index"))

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        return redirect(url_for("dashboard.dashboard_home"))

    flash("Invalid Email or Password", "danger")
    return redirect(url_for("auth.index"))


# Logout
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.index"))