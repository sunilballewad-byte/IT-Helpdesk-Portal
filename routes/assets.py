from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from models import db, Asset

assets = Blueprint("assets", __name__)


# ==========================
# View Assets
# ==========================
@assets.route("/assets")
@login_required
def view_assets():

    # Admin Only
    if current_user.role != "Admin":
        abort(403)

    asset_list = Asset.query.all()

    return render_template(
        "view_assets.html",
        assets=asset_list
    )


# ==========================
# Create Asset
# ==========================
@assets.route("/assets/create", methods=["GET", "POST"])
@login_required
def create_asset():

    # Admin Only
    if current_user.role != "Admin":
        abort(403)

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

    # Admin Only
    if current_user.role != "Admin":
        abort(403)

    asset = Asset.query.get_or_404(id)

    if request.method == "POST":

        asset.asset_id = request.form.get("asset_id")
        asset.asset_name = request.form.get("asset_name")
        asset.asset_type = request.form.get("asset_type")
        asset.brand = request.form.get("brand")
        asset.model = request.form.get("model")
        asset.serial_number = request.form.get("serial_number")
        asset.assigned_to = request.form.get("assigned_to")
        asset.department = request.form.get("department")
        asset.purchase_date = request.form.get("purchase_date") or None
        asset.warranty_end = request.form.get("warranty_end") or None
        asset.status = request.form.get("status")
        asset.remarks = request.form.get("remarks")

        db.session.commit()

        return redirect(url_for("assets.view_assets"))

    return render_template(
        "edit_asset.html",
        asset=asset
    )


# ==========================
# Delete Asset
# ==========================
@assets.route("/assets/delete/<int:id>")
@login_required
def delete_asset(id):

    # Admin Only
    if current_user.role != "Admin":
        abort(403)

    asset = Asset.query.get_or_404(id)

    db.session.delete(asset)
    db.session.commit()

    return redirect(url_for("assets.view_assets"))