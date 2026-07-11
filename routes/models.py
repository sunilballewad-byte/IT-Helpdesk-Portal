from datetime import datetime
from zoneinfo import ZoneInfo

from your_app import db


def india_now():
    return datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).replace(tzinfo=None)



# =========================
# Asset Assignment Model
# =========================

class AssetAssignment(db.Model):

    __tablename__ = "asset_assignments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    asset_id = db.Column(
        db.Integer,
        db.ForeignKey("asset.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    assigned_date = db.Column(
        db.DateTime,
        nullable=False,
        default=india_now
    )

    returned_date = db.Column(
        db.DateTime,
        nullable=True
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Assigned"
    )


    asset = db.relationship(
        "Asset",
        backref=db.backref(
            "assignments",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )


    user = db.relationship(
        "User",
        backref=db.backref(
            "asset_assignments",
            lazy=True
        )
    )


    def __repr__(self):

        return (
            f"<AssetAssignment "
            f"Asset={self.asset_id}, "
            f"User={self.user_id}, "
            f"Status={self.status}>"
        )



# =========================
# Ticket Model
# =========================

class Ticket(db.Model):

    __tablename__ = "tickets"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    ticket_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )


    title = db.Column(
        db.String(200),
        nullable=False
    )


    description = db.Column(
        db.Text,
        nullable=False
    )


    category = db.Column(
        db.String(100),
        nullable=True
    )


    priority = db.Column(
        db.String(50),
        nullable=False,
        default="Medium"
    )


    status = db.Column(
        db.String(50),
        nullable=False,
        default="Open"
    )


    created_by = db.Column(
        db.String(120),
        nullable=True
    )


    assigned_to = db.Column(
        db.String(120),
        nullable=True
    )


    attachment = db.Column(
        db.String(255),
        nullable=True
    )


    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=india_now
    )


    def __repr__(self):

        return (
            f"<Ticket {self.ticket_number}>"
        )



# =========================
# Ticket Comment Model
# =========================

class TicketComment(db.Model):

    __tablename__ = "ticket_comments"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    ticket_id = db.Column(
        db.Integer,
        db.ForeignKey("tickets.id"),
        nullable=False
    )


    comment = db.Column(
        db.Text,
        nullable=False
    )


    created_by = db.Column(
        db.String(120),
        nullable=False
    )


    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=india_now
    )


    ticket = db.relationship(
        "Ticket",
        backref=db.backref(
            "comments",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )


    def __repr__(self):

        return (
            f"<TicketComment {self.id}>"
        )
    # =========================
# Ticket Activity Model
# =========================

class TicketActivity(db.Model):
    __tablename__ = "ticket_activities"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    ticket_id = db.Column(
        db.Integer,
        db.ForeignKey("tickets.id"),
        nullable=False
    )

    action = db.Column(
        db.String(255),
        nullable=False
    )

    performed_by = db.Column(
        db.String(120),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )

    ticket = db.relationship(
        "Ticket",
        backref=db.backref(
            "activities",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    def __repr__(self):
        return f"<TicketActivity {self.id}>"