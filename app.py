from flask import Flask
from config import Config
from models import db

from routes.auth import auth
from routes.dashboard import dashboard
from routes.tickets import tickets

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(tickets)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)