from app import app
from models import db, User
from werkzeug.security import generate_password_hash

with app.app_context():

    User.query.delete()
    db.session.commit()

    admin = User(
        employee_id="EMP001",
        name="Administrator",
        email="admin@helpdesk.com",
        password=generate_password_hash("Admin@123"),
        role="Admin"
    )

    db.session.add(admin)
    db.session.commit()

    print("Admin User Created Successfully")