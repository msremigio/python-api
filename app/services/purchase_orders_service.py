from flask import jsonify, abort
from app.extensions import db
from app.models.purchase_orders import PurchaseOrdersModel


class PurchaseOrdersService:
    @staticmethod
    def get_all():
        purchase_orders = db.session.query(PurchaseOrdersModel).all()
        if purchase_orders:
            return jsonify([po.to_dict() for po in purchase_orders])
        return abort(404, description=f"No purchase orders found.")
    
    @staticmethod
    def get_by_id(id):
        purchase_order = db.session.get(PurchaseOrdersModel, id)
        if purchase_order:
            return jsonify(purchase_order.to_dict())
        abort(404, description=f"No order found for id {id}.")

    @staticmethod
    def post_all(request_data):
        if type(request_data) != list:
            return abort(400, description="Use an array to POST one or many purchase orders.")
        for po in request_data:
            new_order = PurchaseOrdersModel(description=po['description'])
        try:
            db.session.add(new_order)
            db.session.commit()        
        except Exception as e:
            db.session.rollback()
            return abort(400, description=f"{e}")
        return jsonify(request_data)    