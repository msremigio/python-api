from flask import jsonify, abort
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models.purchase_orders_items import PurchaseOrdersItemsModel


class PurchaseOrdersItemsService:
    @staticmethod
    def get_all_by_id(id):
        purchase_order_items = PurchaseOrdersItemsModel.query.filter_by(purchase_order_id=id).all()
        if purchase_order_items:
            return jsonify([po_item.to_dict() for po_item in purchase_order_items])
        return abort(404, description=f"No items found for the purchase order of id {id}.")
    
    @staticmethod
    def post_all_by_id(id, request_data):
        if type(request_data) != list:
            return abort(400, description="An order expects an array of item(s).")
        for po_item in request_data:
            new_order_item = PurchaseOrdersItemsModel(description=po_item['description'], price=po_item['price'], quantity=po_item['quantity'], purchase_order_id=id)
        try:
            db.session.add(new_order_item)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return abort(404, description=f"No order found for id {id}.")
        except Exception as e:
            db.session.rollback()
            return abort(400, description=f"{e}")        
        return jsonify(request_data)
