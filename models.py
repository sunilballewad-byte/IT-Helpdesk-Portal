from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


# =========================
# User Model
# =========================
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), nullable=False, default="Employee")
    department = db.Column(db.String(100))
    mobile = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<User {self.email}>"


# =========================
# Ticket Model
# =========================
class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)

    category = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(20), nullable=False)

    status = db.Column(db.String(20), default="Open")

    created_by = db.Column(db.String(100))
    assigned_to = db.Column(db.String(100))

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )

    def __repr__(self):
        return f"<Ticket {self.ticket_number}>"


# =========================
# Asset Model
# =========================
class Asset(db.Model):
    __tablename__ = "assets"

    id = db.Column(db.Integer, primary_key=True)

    asset_id = db.Column(db.String(30), unique=True, nullable=False)
    asset_name = db.Column(db.String(100), nullable=False)
    asset_type = db.Column(db.String(50), nullable=False)

    brand = db.Column(db.String(50))
    model = db.Column(db.String(100))
    serial_number = db.Column(db.String(100), unique=True)

    assigned_to = db.Column(db.String(100))
    department = db.Column(db.String(100))

    purchase_date = db.Column(db.Date)
    warranty_end = db.Column(db.Date)

    status = db.Column(db.String(30), default="Available")

    remarks = db.Column(db.Text)

    def __repr__(self):
        return f"<Asset {self.asset_id}>"