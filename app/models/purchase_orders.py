from app.extensions import db

class PurchaseOrdersModel(db.Model):
    __tablename__ = 'purchase_orders'

    id = db.Column(db.Integer, primary_key=True, index=True)
    description = db.Column(db.String(500), nullable=False)