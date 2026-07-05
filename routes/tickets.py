from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import or_
from models import db, Ticket
import random

tickets = Blueprint("tickets", __name__)


@tickets.route("/tickets")
def view_tickets():
    search = request.args.get("search", "").strip()

    if search:
        ticket_list = Ticket.query.filter(
            or_(
                Ticket.title.contains(search),
                Ticket.ticket_number.contains(search),
                Ticket.category.contains(search)
            )
        ).order_by(Ticket.id.desc()).all()
    else:
        ticket_list = Ticket.query.order_by(Ticket.id.desc()).all()

    return render_template(
        "view_tickets.html",
        tickets=ticket_list,
        search=search
    )


@tickets.route("/tickets/create", methods=["GET", "POST"])
def create_ticket():
    if request.method == "POST":
        ticket = Ticket(
            ticket_number=f"INC{random.randint(10000, 99999)}",
            title=request.form["title"],
            description=request.form["description"],
            category=request.form["category"],
            priority=request.form["priority"],
            status="Open",
            created_by="Admin"
        )

        db.session.add(ticket)
        db.session.commit()

        return redirect(url_for("tickets.view_tickets"))

    return render_template("create_ticket.html")


@tickets.route("/tickets/edit/<int:id>", methods=["GET", "POST"])
def edit_ticket(id):
    ticket = Ticket.query.get_or_404(id)

    if request.method == "POST":
        ticket.title = request.form["title"]
        ticket.description = request.form["description"]
        ticket.category = request.form["category"]
        ticket.priority = request.form["priority"]
        ticket.status = request.form["status"]

        db.session.commit()

        return redirect(url_for("tickets.view_tickets"))

    return render_template(
        "edit_ticket.html",
        ticket=ticket
    )


@tickets.route("/tickets/delete/<int:id>", methods=["GET", "POST"])
def delete_ticket(id):
    ticket = Ticket.query.get_or_404(id)

    db.session.delete(ticket)
    db.session.commit()

    return redirect(url_for("tickets.view_tickets"))