from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from flask import send_file
from openpyxl import Workbook
from io import BytesIO
from models import Ticket, Asset, User

reports = Blueprint("reports", __name__)

@reports.route("/reports/tickets/excel")
@login_required
def export_ticket_excel():

    if current_user.role != "Admin":
        abort(403)

    wb = Workbook()
    ws = wb.active

    ws.title = "Tickets"

    ws.append([
        "Ticket No",
        "Title",
        "Category",
        "Priority",
        "Status",
        "Created By"
    ])

    tickets = Ticket.query.all()

    for ticket in tickets:

        ws.append([
            ticket.ticket_number,
            ticket.title,
            ticket.category,
            ticket.priority,
            ticket.status,
            ticket.created_by
        ])

    output = BytesIO()

    wb.save(output)

    output.seek(0)

    return send_file(
        output,
        download_name="Tickets_Report.xlsx",
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
@reports.route("/reports")
@login_required
def reports_dashboard():

    if current_user.role != "Admin":
        abort(403)

    total_tickets = Ticket.query.count()
    open_tickets = Ticket.query.filter_by(status="Open").count()
    closed_tickets = Ticket.query.filter_by(status="Closed").count()
    pending_tickets = Ticket.query.filter_by(status="Pending").count()

    total_assets = Asset.query.count()
    total_users = User.query.count()

    return render_template(
        "reports.html",
        total_tickets=total_tickets,
        open_tickets=open_tickets,
        closed_tickets=closed_tickets,
        pending_tickets=pending_tickets,
        total_assets=total_assets,
        total_users=total_users
    )