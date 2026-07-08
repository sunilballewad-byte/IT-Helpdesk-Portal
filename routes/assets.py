from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from models import db, Asset, User

assets = Blueprint("assets", __name__)


# ==========================
# View Assets
# ==========================
@assets.route("/assets")
@login_required
def view_assets():

    if current_user.role != "Admin":
        abort(403)

    assets_list = Asset.query.all()

    return render_template(
        "view_assets.html",
        assets=assets_list
    )


# ==========================
# Create Asset
# ==========================
@assets.route("/assets/create", methods=["GET", "POST"])
@login_required
def create_asset():

    if current_user.role != "Admin":
        abort(403)

    if request.method == "POST":

        purchase_date = request.form.get("purchase_date")
        warranty_end = request.form.get("warranty_end")

        purchase_date = (
            datetime.strptime(purchase_date, "%Y-%m-%d").date()
            if purchase_date else None
        )

        warranty_end = (
            datetime.strptime(warranty_end, "%Y-%m-%d").date()
            if warranty_end else None
        )

        asset = Asset(
            asset_id=request.form.get("asset_id"),
            asset_name=request.form.get("asset_name"),
            asset_type=request.form.get("asset_type"),
            brand=request.form.get("brand"),
            model=request.form.get("model"),
            serial_number=request.form.get("serial_number"),
            assigned_to=request.form.get("assigned_to"),
            department=request.form.get("department"),
            purchase_date=purchase_date,
            warranty_end=warranty_end,
            status=request.form.get("status"),
            remarks=request.form.get("remarks")
        )

        db.session.add(asset)
        db.session.commit()

        return redirect(url_for("assets.view_assets"))

    return render_template("create_asset.html")


# ==========================
# Edit Asset
# ==========================
@assets.route("/assets/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_asset(id):

    if current_user.role != "Admin":
        abort(403)

    asset = Asset.query.get_or_404(id)

    if request.method == "POST":

        purchase_date = request.form.get("purchase_date")
        warranty_end = request.form.get("warranty_end")

        asset.asset_id = request.form.get("asset_id")
        asset.asset_name = request.form.get("asset_name")
        asset.asset_type = request.form.get("asset_type")
        asset.brand = request.form.get("brand")
        asset.model = request.form.get("model")
        asset.serial_number = request.form.get("serial_number")
        asset.assigned_to = request.form.get("assigned_to")
        asset.department = request.form.get("department")

        asset.purchase_date = (
            datetime.strptime(purchase_date, "%Y-%m-%d").date()
            if purchase_date else None
        )

        asset.warranty_end = (
            datetime.strptime(warranty_end, "%Y-%m-%d").date()
            if warranty_end else None
        )

        asset.status = request.form.get("status")
        asset.remarks = request.form.get("remarks")

        db.session.commit()

        return redirect(url_for("assets.view_assets"))

    return render_template(
        "edit_asset.html",
        asset=asset
    )


# ==========================
# Assign Asset
# ==========================
@assets.route("/assets/assign/<int:id>", methods=["GET", "POST"])
@login_required
def assign_asset(id):

    if current_user.role != "Admin":
        abort(403)

    asset = Asset.query.get_or_404(id)

    users = User.query.all()

    if request.method == "POST":

        user_id = request.form.get("user_id")

        user = User.query.get_or_404(user_id)

        assignment = AssetAssignment(
            asset_id=asset.id,
            user_id=user.id
        )

        asset.assigned_to = user.name
        asset.status = "Assigned"

        db.session.add(assignment)
        db.session.commit()

        return redirect(url_for("assets.view_assets"))

    return render_template(
        "assign_asset.html",
        asset=asset,
        users=users
    )


# ==========================
# Delete Asset
# ==========================
@assets.route("/assets/delete/<int:id>")
@login_required
def delete_asset(id):

    if current_user.role != "Admin":
        abort(403)

    asset = Asset.query.get_or_404(id)

    db.session.delete(asset)
    db.session.commit()

    return redirect(url_for("assets.view_assets"))