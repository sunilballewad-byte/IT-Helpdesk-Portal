from flask import Blueprint, render_template, request, redirect, url_for

from models import db, Ticket

tickets = Blueprint("tickets", __name__)


@tickets.route("/tickets/create", methods=["GET", "POST"])
def create_ticket():

    if request.method == "POST":

        ticket = Ticket(
            ticket_number="INC0001",
            title=request.form["title"],
            description=request.form["description"],
            category=request.form["category"],
            priority=request.form["priority"],
            created_by="Admin"
        )

        db.session.add(ticket)
        db.session.commit()

        return redirect(url_for("tickets.view_tickets"))

    return render_template("create_ticket.html")


@tickets.route("/tickets")
def view_tickets():

    all_tickets = Ticket.query.all()

    return render_template(
        "view_tickets.html",
        tickets=all_tickets
    )