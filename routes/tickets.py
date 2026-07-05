from flask import Blueprint, render_template

tickets = Blueprint("tickets", __name__)

@tickets.route("/tickets/create")
def create_ticket():
    return render_template("create_ticket.html")


@tickets.route("/tickets")
def view_tickets():
    return render_template("view_tickets.html")