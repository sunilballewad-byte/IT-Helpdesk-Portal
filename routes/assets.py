from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

from models import db, Asset

assets = Blueprint("assets", __name__)


@assets.route("/assets")
@login_required
def view_assets():

    asset_list = Asset.query.all()

    return render_template(
        "view_assets.html",
        assets=asset_list
    )


@assets.route("/assets/create", methods=["GET", "POST"])
@login_required
def create_asset():

    if request.method == "POST":

        asset = Asset(
            asset_id=request.form.get("asset_id"),
            asset_name=request.form.get("asset_name"),
            asset_type=request.form.get("asset_type"),
            brand=request.form.get("brand"),
            model=request.form.get("model"),
            serial_number=request.form.get("serial_number"),
            assigned_to=request.form.get("assigned_to"),
            department=request.form.get("department"),
            purchase_date=request.form.get("purchase_date") or None,
            warranty_end=request.form.get("warranty_end") or None,
            status=request.form.get("status"),
            remarks=request.form.get("remarks"),
        )

        db.session.add(asset)
        db.session.commit()

        return redirect(url_for("assets.view_assets"))

    return render_template("create_asset.html")