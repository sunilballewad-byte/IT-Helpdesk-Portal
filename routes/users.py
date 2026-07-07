from functools import wraps

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from models import db, User

users = Blueprint("users", __name__)


# =====================================
# Admin Access Decorator
# =====================================
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != "Admin":
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


# =====================================
# View Users
# =====================================
@users.route("/users")
@admin_required
def view_users():
    user_list = User.query.order_by(User.id.desc()).all()

    return render_template(
        "view_users.html",
        users=user_list,
    )


# =====================================
# Create User
# =====================================
@users.route("/users/create", methods=["GET", "POST"])
@admin_required
def create_user():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        employee_id = request.form.get("employee_id", "").strip()

        if User.query.filter_by(email=email).first():
            flash("Email already exists.", "danger")
            return redirect(url_for("users.create_user"))

        if User.query.filter_by(employee_id=employee_id).first():
            flash("Employee ID already exists.", "danger")
            return redirect(url_for("users.create_user"))

        user = User(
            employee_id=employee_id,
            name=request.form.get("name", "").strip(),
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
@admin_required
def edit_user(id):

    user = User.query.get_or_404(id)

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        employee_id = request.form.get("employee_id", "").strip()

        # Prevent duplicate email
        existing_email = User.query.filter(
            User.email == email,
            User.id != user.id
        ).first()

        if existing_email:
            flash("Email already exists.", "danger")
            return redirect(url_for("users.edit_user", id=id))

        # Prevent duplicate employee ID
        existing_emp = User.query.filter(
            User.employee_id == employee_id,
            User.id != user.id
        ).first()

        if existing_emp:
            flash("Employee ID already exists.", "danger")
            return redirect(url_for("users.edit_user", id=id))

        user.employee_id = employee_id
        user.name = request.form.get("name", "").strip()
        user.email = email
        user.department = request.form.get("department")
        user.mobile = request.form.get("mobile")
        user.role = request.form.get("role")

        password = request.form.get("password")
        if password:
            user.password = generate_password_hash(password)

        db.session.commit()

        flash("User updated successfully.", "success")
        return redirect(url_for("users.view_users"))

    return render_template(
        "edit_user.html",
        user=user,
    )


# =====================================
# Delete User
# =====================================
@users.route("/users/delete/<int:id>", methods=["POST"])
@admin_required
def delete_user(id):

    user = User.query.get_or_404(id)

    # Prevent deleting yourself
    if user.id == current_user.id:
        flash("You cannot delete your own account.", "danger")
        return redirect(url_for("users.view_users"))

    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully.", "success")
    return redirect(url_for("users.view_users"))