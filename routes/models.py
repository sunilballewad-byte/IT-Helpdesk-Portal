class AssetAssignment(db.Model):
    __tablename__ = "asset_assignments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    asset_id = db.Column(
        db.Integer,
        db.ForeignKey("asset.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    assigned_date = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp()
    )

    returned_date = db.Column(
        db.DateTime,
        nullable=True
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Assigned"
    )

    # Relationships
    asset = db.relationship(
        "Asset",
        backref=db.backref(
            "assignments",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "asset_assignments",
            lazy=True
        )
    )

    def __repr__(self):
        return (
            f"<AssetAssignment "
            f"Asset={self.asset_id}, "
            f"User={self.user_id}, "
            f"Status={self.status}>"
        )
