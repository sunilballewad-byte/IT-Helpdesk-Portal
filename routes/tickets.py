import os
from datetime import datetime, timedelta
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
# Helper: Auto Escalate Overdue Tickets
# =====================================
def process_sla_escalations():
    now = datetime.utcnow()

    overdue_tickets = Ticket.query.filter(
        Ticket.sla_due_at.isnot(None),
        Ticket.sla_due_at < now,
        ~Ticket.status.in_(["Resolved", "Closed"])
    ).all()

    changed = False

    for ticket in overdue_tickets:
        overdue_hours = (
            now - ticket.sla_due_at
        ).total_seconds() / 3600

        if overdue_hours >= 24:
            new_level = 3
        elif overdue_hours >= 4:
            new_level = 2
        else:
            new_level = 1

        if ticket.escalation_level < new_level:
            ticket.escalation_level = new_level

            if ticket.escalated_at is None:
                ticket.escalated_at = now

            action_text = (
                f"ESCALATED Level {new_level} - "
                f"SLA breached for {ticket.ticket_number}"
            )

            existing_activity = TicketActivity.query.filter_by(
                ticket_id=ticket.id,
                action=action_text
            ).first()

            if not existing_activity:
                activity = TicketActivity(
                    ticket_id=ticket.id,
                    action=action_text,
                    performed_by="System"
                )

                db.session.add(activity)

            changed = True

    if changed:
        db.session.commit()
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
    process_sla_escalations()
    search = request.args.get("search", "").strip()
    ticket_filter = request.args.get("filter", "").strip()

    query = Ticket.query

    if not is_admin():
        query = query.filter(Ticket.created_by == current_user.email)
    if ticket_filter == "escalated":
        query = query.filter(
            Ticket.escalated_at.isnot(None),
            ~Ticket.status.in_(["Resolved", "Closed"])
        )
    elif ticket_filter == "active_sla":
        query = query.filter(
            Ticket.sla_due_at.isnot(None),
            Ticket.sla_due_at >= datetime.utcnow(),
            ~Ticket.status.in_(["Resolved", "Closed"])
        )

    elif ticket_filter == "overdue_sla":
        query = query.filter(
            Ticket.sla_due_at.isnot(None),
            Ticket.sla_due_at < datetime.utcnow(),
            ~Ticket.status.in_(["Resolved", "Closed"])
        )

    elif ticket_filter == "sla_met":
        query = query.filter(
            Ticket.sla_due_at.isnot(None),
            Ticket.resolved_at.isnot(None),
            Ticket.resolved_at <= Ticket.sla_due_at
        )

    elif ticket_filter == "sla_breached":
        query = query.filter(
            Ticket.sla_due_at.isnot(None),
            Ticket.resolved_at.isnot(None),
            Ticket.resolved_at > Ticket.sla_due_at
        )

    elif ticket_filter == "escalation_l1":
        query = query.filter(
            Ticket.escalation_level == 1
        )

    elif ticket_filter == "escalation_l2":
        query = query.filter(
            Ticket.escalation_level == 2
        )

    elif ticket_filter == "escalation_l3":
        query = query.filter(
            Ticket.escalation_level >= 3
        )
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
            search=search,
    ticket_filter=ticket_filter,
    now=datetime.utcnow()
    )


# =====================================
# Create Ticket
# =====================================

@tickets.route(
    "/tickets/create",
    methods=["GET", "POST"]
)
@login_required
def create_ticket():

    if request.method == "POST":

        filename = None

        file = request.files.get("attachment")

        if file and file.filename:

            filename = secure_filename(
                file.filename
            )

            file.save(
                os.path.join(
                    Config.UPLOAD_FOLDER,
                    filename
                )
            )
        priority = request.form.get("priority")

        sla_hours = {
            "Critical": 4,
            "High": 24,
            "Medium": 48,
            "Low": 72
        }

        sla_due_at = datetime.utcnow() + timedelta(
            hours=sla_hours.get(priority, 48)
        )
        ticket = Ticket(
            ticket_number=generate_ticket_number(),
            title=request.form.get("title"),
            description=request.form.get("description"),
            category=request.form.get("category"),
            priority=priority,
            status="Open",
            created_by=current_user.email,
            attachment=filename,
            sla_due_at=sla_due_at
        )

        db.session.add(ticket)

        # First commit generates ticket ID
        db.session.commit()

        log_activity(
            ticket.id,
            f"Ticket {ticket.ticket_number} created"
        )

        db.session.commit()

        return redirect(
            url_for("tickets.view_tickets")
        )

    return render_template(
        "create_ticket.html"
    )

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
    users=users,
    now=datetime.utcnow()
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

@tickets.route(
    "/tickets/<int:id>/assign",
    methods=["POST"]
)
@login_required
def assign_ticket(id):

    if not is_admin():
        abort(403)

    ticket = db.session.get(Ticket, id)

    if not ticket:
        abort(404)

    assigned_to = request.form.get(
        "assigned_to",
        ""
    ).strip()

    # Do nothing if no engineer selected
    if not assigned_to:
        return redirect(
            url_for(
                "tickets.view_tickets"
            )
        )

    old_assigned_to = ticket.assigned_to

    # Do nothing if same engineer already assigned
    if old_assigned_to == assigned_to:
        return redirect(
            url_for(
                "tickets.ticket_details",
                id=ticket.id
            )
        )

    ticket.assigned_to = assigned_to

    if old_assigned_to:

        log_activity(
            ticket.id,
            f"Ticket reassigned from {old_assigned_to} to {assigned_to}"
        )

    else:

        log_activity(
            ticket.id,
            f"Ticket assigned to {assigned_to}"
        )

    db.session.commit()

    return redirect(
        url_for(
            "tickets.ticket_details",
            id=ticket.id
        )
    )
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

        # Set resolved date
        if new_status in ["Resolved", "Closed"]:
            ticket.resolved_at = datetime.utcnow()

        elif old_status in ["Resolved", "Closed"]:
            ticket.resolved_at = None

        log_activity(
            ticket.id,
            f"Status changed from {old_status} to {new_status}"
        )

        db.session.commit()

    return redirect(
        url_for("tickets.ticket_details", id=id)
    )


# =====================================
# Edit Ticket
# =====================================

@tickets.route(
    "/tickets/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_ticket(id):

    if not is_admin():
        abort(403)

    ticket = db.session.get(Ticket, id)

    if not ticket:
        abort(404)

    if request.method == "POST":

        old_title = ticket.title
        old_priority = ticket.priority

        ticket.title = request.form.get("title")
        ticket.description = request.form.get("description")
        ticket.category = request.form.get("category")
        ticket.priority = request.form.get("priority")

        log_activity(
            ticket.id,
            f"Ticket edited. Priority changed from {old_priority} to {ticket.priority}"
        )

        db.session.commit()

        return redirect(
            url_for(
                "tickets.ticket_details",
                id=ticket.id
            )
        )

    return render_template(
        "edit_ticket.html",
        ticket=ticket
    )
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
# =====================================
# Download Ticket Attachment
# =====================================

@tickets.route(
    "/tickets/<int:id>/attachment"
)
@login_required
def download_attachment(id):

    ticket = db.session.get(
        Ticket,
        id
    )

    if not ticket:
        abort(404)

    if (
        not is_admin()
        and ticket.created_by != current_user.email
    ):
        abort(403)

    if not ticket.attachment:
        abort(404)

    return send_from_directory(
        Config.UPLOAD_FOLDER,
        ticket.attachment,
        as_attachment=True
    )
