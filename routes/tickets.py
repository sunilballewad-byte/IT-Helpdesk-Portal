import os

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    abort,
    send_from_directory
)
from flask_login import login_required, current_user
from sqlalchemy import or_
from werkzeug.utils import secure_filename

from models import db, Ticket, TicketComment, TicketActivity, User
from config import Config


tickets = Blueprint("tickets", __name__)


# =====================================
# Helper: Check Admin
# =====================================
def is_admin():
    return current_user.role and current_user.role.lower() == "admin"


# =====================================
# Helper: Ticket Activity Logger
# =====================================
def log_activity(ticket_id, action):
    activity = TicketActivity(
        ticket_id=ticket_id,
        action=action,
        performed_by=current_user.email
    )
    db.session.add(activity)


# =====================================
# Helper: Generate Ticket Number
# =====================================
def generate_ticket_number():
    last_ticket = Ticket.query.order_by(Ticket.id.desc()).first()

    if not last_ticket:
        return "#0001"

    try:
        number = int(last_ticket.ticket_number.replace("#", ""))
        return f"#{number + 1:04d}"
    except Exception:
        return "#0001"


# =====================================
# View Tickets
# =====================================
@tickets.route("/tickets")
@login_required
def view_tickets():
    search = request.args.get("search", "").strip()
    query = Ticket.query

    if not is_admin():
        query = query.filter(Ticket.created_by == current_user.email)

    if search:
        query = query.filter(
            or_(
                Ticket.ticket_number.ilike(f"%{search}%"),
                Ticket.title.ilike(f"%{search}%"),
                Ticket.category.ilike(f"%{search}%"),
                Ticket.priority.ilike(f"%{search}%"),
                Ticket.status.ilike(f"%{search}%")
            )
        )

    tickets_list = query.order_by(Ticket.id.desc()).all()

    return render_template(
        "view_tickets.html",
        tickets=tickets_list,
        search=search
    )


# =====================================
# Create Ticket
# =====================================
@tickets.route("/tickets/create", methods=["GET", "POST"])
@login_required
def create_ticket():
    if request.method == "POST":
        filename = None
        file = request.files.get("attachment")

        if file and file.filename:
            filename = secure_filename(file.filename)
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            file.save(os.path.join(Config.UPLOAD_FOLDER, filename))

        ticket = Ticket(
            ticket_number=generate_ticket_number(),
            title=request.form.get("title"),
            description=request.form.get("description"),
            category=request.form.get("category"),
            priority=request.form.get("priority", "Medium"),
            status="Open",
            created_by=current_user.email,
            attachment=filename
        )

        db.session.add(ticket)
        db.session.commit()  # Commit first to generate the ticket ID 

        # Now log the creation activity using the new ticket ID
        log_activity(ticket.id, "Ticket created")
        db.session.commit()

        return redirect(url_for("tickets.view_tickets"))

    return render_template("create_ticket.html")


# =====================================
# Ticket Details
# =====================================
@tickets.route("/tickets/<int:id>")
@login_required
def ticket_details(id):
    ticket = db.session.get(Ticket, id)

    if not ticket:
        abort(404)

    if not is_admin() and ticket.created_by != current_user.email:
        abort(403)

    users = User.query.filter(User.is_active.is_(True)).order_by(User.name.asc()).all()

    return render_template(
        "ticket_details.html",
        ticket=ticket,
        users=users
    )


# =====================================
# Add Comment
# =====================================
@tickets.route("/tickets/<int:id>/comment", methods=["POST"])
@login_required
def add_comment(id):
    ticket = db.session.get(Ticket, id)

    if not ticket:
        abort(404)

    if not is_admin() and ticket.created_by != current_user.email:
        abort(403)

    comment_text = request.form.get("comment", "").strip()

    if comment_text:
        comment = TicketComment(
            ticket_id=ticket.id,
            comment=comment_text,
            created_by=current_user.email
        )
        db.session.add(comment)
        
        # Log the activity
        log_activity(ticket.id, "Added a comment / work note")
        db.session.commit()

    return redirect(url_for("tickets.ticket_details", id=ticket.id))


# =====================================
# Assign Ticket
# =====================================
@tickets.route("/tickets/<int:id>/assign", methods=["POST"])
@login_required
def assign_ticket(id):
    if not is_admin():
        abort(403)

    ticket = db.session.get(Ticket, id)

    if not ticket:
        abort(404)

    assigned_to = request.form.get("assigned_to", "").strip()
    ticket.assigned_to = assigned_to if assigned_to else None

    # Log the activity
    log_activity(
        ticket.id,
        f"Ticket assigned to {ticket.assigned_to or 'Unassigned'}"
    )
    db.session.commit()

    return redirect(url_for("tickets.ticket_details", id=ticket.id))


# =====================================
# Update Ticket Status
# =====================================
@tickets.route("/tickets/<int:id>/status", methods=["POST"])
@login_required
def update_status(id):
    if not is_admin():
        abort(403)

    ticket = db.session.get(Ticket, id)

    if not ticket:
        abort(404)

    old_status = ticket.status
    new_status = request.form.get("status")

    if new_status and old_status != new_status:
        ticket.status = new_status
        
        # Log the activity
        log_activity(
            ticket.id,
            f"Status changed from {old_status} to {new_status}"
        )
        db.session.commit()

    return redirect(url_for("tickets.ticket_details", id=id))


# =====================================
# Edit Ticket
# =====================================
@tickets.route("/tickets/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_ticket(id):
    if not is_admin():
        abort(403)

    ticket = db.session.get(Ticket, id)

    if not ticket:
        abort(404)

    if request.method == "POST":
        ticket.title = request.form.get("title")
        ticket.description = request.form.get("description")
        ticket.category = request.form.get("category")
        ticket.priority = request.form.get("priority")
        # =====================================
# Delete Ticket
# =====================================

@tickets.route(
    "/tickets/delete/<int:id>",
    methods=["POST"]
)
@login_required
def delete_ticket(id):

    if not is_admin():
        abort(403)

    ticket = db.session.get(
        Ticket,
        id
    )

    if not ticket:
        abort(404)

    db.session.delete(ticket)
    db.session.commit()

    return redirect(
        url_for("tickets.view_tickets")
    )