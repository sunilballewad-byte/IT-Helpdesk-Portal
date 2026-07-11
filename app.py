from flask import Flask, render_template
from flask_login import LoginManager
from datetime import datetime, timedelta
from config import Config
from models import db, User

from routes.auth import auth
from routes.dashboard import dashboard
from routes.tickets import tickets
from routes.admin import admin
from routes.assets import assets
from routes.users import users
from routes.reports import reports
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.index"
@app.template_filter("ist")
def convert_to_ist(value):

    if value is None:
        return "-"

    ist_time = value + timedelta(
        hours=5,
        minutes=30
    )

    return ist_time.strftime(
        "%d-%m-%Y %I:%M %p"
    )
@app.template_filter("sla_remaining")
def sla_remaining(value):

    if value is None:
        return "SLA not available"

    difference = value - datetime.utcnow()

    total_minutes = int(
        abs(difference.total_seconds()) // 60
    )

    hours = total_minutes // 60
    minutes = total_minutes % 60

    if difference.total_seconds() < 0:
        return f"{hours}h {minutes}m overdue"

    return f"{hours}h {minutes}m remaining"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -------------------------------
# Error Pages
# -------------------------------
@app.errorhandler(403)
def forbidden(error):
    return render_template("errors/403.html"), 403


# -------------------------------
# Register Blueprints
# -------------------------------
app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(tickets)
app.register_blueprint(admin)
app.register_blueprint(assets)
app.register_blueprint(users)
app.register_blueprint(reports)


# -------------------------------
# Create Database
# -------------------------------


if __name__ == "__main__":
    app.run(debug=True)