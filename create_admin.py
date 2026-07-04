from app import app
from models import db, User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

with app.app_context():

    admin = User.query.filter_by(email="admin@helpdesk.com").first()

    if not admin:

        password = bcrypt.generate_password_hash("Admin@123").decode("utf-8")

        admin = User(
            employee_id="EMP001",
            name="Administrator",
            email="admin@helpdesk.com",
            password=password,
            role="Admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin User Created Successfully")

    else:

        print("Admin Already Exists")