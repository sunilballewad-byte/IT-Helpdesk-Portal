from flask import Blueprint, render_template
from flask_login import login_required
from models import User

users = Blueprint("users", __name__)


@users.route("/users")
@login_required
def view_users():

    user_list = User.query.order_by(User.id.desc()).all()

    return render_template(
        "view_users.html",
        users=user_list
    )