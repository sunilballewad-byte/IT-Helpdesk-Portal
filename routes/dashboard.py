from flask import Blueprint, render_template
from flask_login import login_required
from datetime import datetime
from models import Ticket, Asset

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
@login_required
def dashboard_home():

    # ---------------- Tickets ----------------
    total_tickets = Ticket.query.count()

    open_tickets = Ticket.query.filter_by(status="Open").count()

    closed_tickets = Ticket.query.filter_by(status="Closed").count()

    pending_tickets = Ticket.query.filter_by(status="Pending").count()

    # ---------------- SLA Summary ----------------
    now = datetime.utcnow()

    active_sla = Ticket.query.filter(
        Ticket.sla_due_at.isnot(None),
        Ticket.sla_due_at >= now,
        ~Ticket.status.in_(["Resolved", "Closed"])
    ).count()

    overdue_sla = Ticket.query.filter(
        Ticket.sla_due_at.isnot(None),
        Ticket.sla_due_at < now,
        ~Ticket.status.in_(["Resolved", "Closed"])
    ).count()

    critical_tickets = Ticket.query.filter_by(
        priority="Critical"
    ).count()

    sla_met = Ticket.query.filter(
        Ticket.sla_due_at.isnot(None),
        Ticket.resolved_at.isnot(None),
        Ticket.resolved_at <= Ticket.sla_due_at
    ).count()

    sla_breached = Ticket.query.filter(
        Ticket.sla_due_at.isnot(None),
        Ticket.resolved_at.isnot(None),
        Ticket.resolved_at > Ticket.sla_due_at
    ).count()

    total_completed_sla = sla_met + sla_breached

    if total_completed_sla > 0:
        sla_compliance = round(
            (sla_met / total_completed_sla) * 100,
            1
        )
    else:
        sla_compliance = 0
    # ---------------- Assets ----------------
    total_assets = Asset.query.count()

    assigned_assets = Asset.query.filter_by(status="Assigned").count()

    available_assets = Asset.query.filter_by(status="Available").count()

    repair_assets = Asset.query.filter_by(status="Repair").count()

    # ---------------- Recent Tickets ----------------
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

        recent_tickets=recent_tickets,

        active_sla=active_sla,
        overdue_sla=overdue_sla,
        critical_tickets=critical_tickets,
        sla_met=sla_met,
        sla_breached=sla_breached,
                sla_compliance=sla_compliance,
        now=now
    )