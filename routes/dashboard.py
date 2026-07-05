from flask import Blueprint, render_template
from models import Ticket
from flask_login import login_required

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/dashboard")
@login_required
def dashboard_home():
    total = Ticket.query.count()
    open_count = Ticket.query.filter_by(status="Open").count()
    closed_count = Ticket.query.filter_by(status="Closed").count()
    pending_count = Ticket.query.filter_by(status="Pending").count()

    tickets = Ticket.query.order_by(Ticket.id.desc()).limit(5).all()

    return render_template(
        "dashboard.html",
        total=total,
        open_count=open_count,
        closed_count=closed_count,
        pending_count=pending_count,
        tickets=tickets
    )