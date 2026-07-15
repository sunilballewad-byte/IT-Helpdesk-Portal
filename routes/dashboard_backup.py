from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime
from models import Ticket, Asset

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
@login_required
def dashboard_home():
    is_technician = (
        current_user.role
        and current_user.role.lower() == "technician"
    )
    # ---------------- Tickets ----------------
    ticket_query = Ticket.query

    if is_technician:
        ticket_query = ticket_query.filter(
            Ticket.assigned_to == current_user.email
        )

    total_tickets = ticket_query.count()

    open_tickets = ticket_query.filter_by(
        status="Open"
    ).count()

    closed_tickets = ticket_query.filter_by(
        status="Closed"
    ).count()

    pending_tickets = ticket_query.filter_by(
        status="Pending"
    ).count()

    # ---------------- SLA Summary ----------------
    now = datetime.utcnow()
    sla_query = Ticket.query

    if is_technician:
        sla_query = sla_query.filter(
            Ticket.assigned_to == current_user.email
        )
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
    escalated_tickets = Ticket.query.filter(
        Ticket.escalated_at.isnot(None),
        ~Ticket.status.in_(["Resolved", "Closed"])
    ).count()

    escalation_l1 = Ticket.query.filter_by(
        escalation_level=1
    ).count()

    escalation_l2 = Ticket.query.filter_by(
        escalation_level=2
    ).count()

    escalation_l3 = Ticket.query.filter(
        Ticket.escalation_level >= 3
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
                escalated_tickets=escalated_tickets,
                        escalation_l1=escalation_l1,
        escalation_l2=escalation_l2,
        escalation_l3=escalation_l3,
                sla_compliance=sla_compliance,
        now=now
    )
