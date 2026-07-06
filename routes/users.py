from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from werkzeug.security import generate_password_hash

from models import db, User

users = Blueprint("users", __name__)


# =====================================
# View Users
# =====================================
@users.route("/users")
@login_required
def view_users():
    user_list = User.query.order_by(User.id.desc()).all()

    return render_template(
        "view_users.html",
        users=user_list
    )


# =====================================
# Create User
# =====================================
@users.route("/users/create", methods=["GET", "POST"])
@login_required
def create_user():

    if request.method == "POST":

        email = request.form.get("email")
        employee_id = request.form.get("employee_id")

        # Check duplicate email
        if User.query.filter_by(email=email).first():
            flash("Email already exists.", "danger")
            return redirect(url_for("users.create_user"))

        # Check duplicate employee ID
        if User.query.filter_by(employee_id=employee_id).first():
            flash("Employee ID already exists.", "danger")
            return redirect(url_for("users.create_user"))

        user = User(
            employee_id=employee_id,
            name=request.form.get("name"),
            email=email,
            password=generate_password_hash(request.form.get("password")),
            role=request.form.get("role"),
            department=request.form.get("department"),
            mobile=request.form.get("mobile"),
        )

        db.session.add(user)
        db.session.commit()

        flash("User created successfully.", "success")
        return redirect(url_for("users.view_users"))

    return render_template("create_user.html")


# =====================================
# Edit User
# =====================================
@users.route("/users/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_user(id):

    user = User.query.get_or_404(id)

    if request.method == "POST":

        user.employee_id = request.form.get("employee_id")
        user.name = request.form.get("name")
        user.email = request.form.get("email")
        user.department = request.form.get("department")
        user.mobile = request.form.get("mobile")
        user.role = request.form.get("role")

        # Update password only if a new password is entered
        password = request.form.get("password")
        if password:
            user.password = generate_password_hash(password)

        db.session.commit()

        flash("User updated successfully.", "success")
        return redirect(url_for("users.view_users"))

    return render_template(
        "edit_user.html",
        user=user
    )


# =====================================
# Delete User
# =====================================
@users.route("/users/delete/<int:id>")
@login_required
def delete_user(id):

    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully.", "success")
    return redirect(url_for("users.view_users"))