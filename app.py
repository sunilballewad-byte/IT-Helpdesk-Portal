from flask import Flask, render_template
from config import Config
from models import db
from routes.auth import auth

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(auth)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)