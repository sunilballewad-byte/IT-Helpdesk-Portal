from flask import Blueprint, render_template
from flask_login import login_required
from models import Ticket, Asset

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
@login_required
def dashboard_home():

    total_tickets = Ticket.query.count()

    open_tickets = Ticket.query.filter_by(status="Open").count()

    closed_tickets = Ticket.query.filter_by(status="Closed").count()

    pending_tickets = Ticket.query.filter_by(status="Pending").count()

    total_assets = Asset.query.count()

    assigned_assets = Asset.query.filter_by(status="Assigned").count()

    available_assets = Asset.query.filter_by(status="Available").count()

    repair_assets = Asset.query.filter_by(status="Repair").count()

    recent_tickets = (
        Ticket.query
        .order_by(Ticket.id.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard.html",
        total_tickets=total_tickets,
        open_tickets=open_tickets,
        closed_tickets=closed_tickets,
        pending_tickets=pending_tickets,
        total_assets=total_assets,
        assigned_assets=assigned_assets,
        available_assets=available_assets,
        repair_assets=repair_assets,
        recent_tickets=recent_tickets
    )