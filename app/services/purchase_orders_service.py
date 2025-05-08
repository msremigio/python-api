from flask import jsonify, abort
from app.extensions import db
from app.models.purchase_orders import PurchaseOrdersModel


class PurchaseOrdersService:
    @staticmethod
    def get_purchase_orders():
        purchase_orders = db.session.query(PurchaseOrdersModel).all()
        if purchase_orders:
            return jsonify([po.to_dict() for po in purchase_orders])
        return abort(404, description=f"No purchase orders found.")