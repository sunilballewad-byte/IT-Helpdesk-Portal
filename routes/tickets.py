import os
import random

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from sqlalchemy import or_
from werkzeug.utils import secure_filename

from config import Config
from models import db, Ticket

tickets = Blueprint("tickets", __name__)


# =====================================
# View Tickets
# =====================================
@tickets.route("/tickets")
@login_required
def view_tickets():

    search = request.args.get("search", "").strip()

    query = Ticket.query

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

    ticket_list = query.order_by(Ticket.id.desc()).all()

    return render_template(
        "view_tickets.html",
        tickets=ticket_list,
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

        if file and file.filename != "":

            filename = secure_filename(file.filename)

            file.save(
                os.path.join(
                    Config.UPLOAD_FOLDER,
                    filename
                )
            )

        ticket = Ticket(

            ticket_number=f"INC{random.randint(10000,99999)}",

            title=request.form.get("title"),

            description=request.form.get("description"),

            category=request.form.get("category"),

            priority=request.form.get("priority"),

            status="Open",

            created_by="Admin",

            attachment=filename

        )

        db.session.add(ticket)

        db.session.commit()

        return redirect(url_for("tickets.view_tickets"))

    return render_template("create_ticket.html")


# =====================================
# Edit Ticket
# =====================================
@tickets.route("/tickets/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_ticket(id):

    ticket = Ticket.query.get_or_404(id)

    if request.method == "POST":

        ticket.title = request.form.get("title")

        ticket.description = request.form.get("description")

        ticket.category = request.form.get("category")

        ticket.priority = request.form.get("priority")

        ticket.status = request.form.get("status")

        db.session.commit()

        return redirect(url_for("tickets.view_tickets"))

    return render_template(
        "edit_ticket.html",
        ticket=ticket
    )


# =====================================
# Delete Ticket
# =====================================
@tickets.route("/tickets/delete/<int:id>")
@login_required
def delete_ticket(id):

    ticket = Ticket.query.get_or_404(id)

    db.session.delete(ticket)

    db.session.commit()

    return redirect(url_for("tickets.view_tickets"))