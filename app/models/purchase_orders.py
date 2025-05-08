from app.extensions import db
from app.models.enums import PurchaseOrderStatus

class PurchaseOrdersModel(db.Model):
    __tablename__ = 'purchase_orders'

    id = db.Column(db.Integer, primary_key=True, index=True)
    description = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    status = db.Column(db.Enum(PurchaseOrderStatus, values_callable=lambda sts: [st.value for st in sts]), default=PurchaseOrderStatus.PENDING, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "status": self.status.value
        }