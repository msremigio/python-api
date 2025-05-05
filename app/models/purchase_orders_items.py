from app.extensions import db

class PurchaseOrdersItemsModel(db.Model):
    __tablename__ = 'purchase_orders_items'

    id = db.Column(db.Integer, primary_key=True, index=True)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_orders.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "price": self.price,
            "quantity": self.quantity,
            "purchase_order_id": self.purchase_order_id
        }