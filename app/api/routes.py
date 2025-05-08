from flask import Blueprint, jsonify, request, abort
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.services.purchase_orders_service import PurchaseOrdersService
from app.models.purchase_orders import PurchaseOrdersModel
from app.models.purchase_orders_items import PurchaseOrdersItemsModel


api_blueprint = Blueprint('api', __name__)


@api_blueprint.errorhandler(400)
def bad_request(e):
     return jsonify(error = str(e)), 400

@api_blueprint.errorhandler(404)
def not_found(e):
     return jsonify(error = str(e)), 404

@api_blueprint.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the ***purchase_orders*** API homepage!'})

@api_blueprint.route('/purchase_orders', methods=['GET'])
def get_purchase_orders():  
    return PurchaseOrdersService.get_purchase_orders()

@api_blueprint.route('/purchase_orders/<int:id>', methods=['GET'])
def get_purchase_orders_by_id(id):
    purchase_order = db.session.get(PurchaseOrdersModel, id)
    if purchase_order:
        return jsonify(purchase_order.to_dict())
    abort(404, description=f"No order found for id {id}.")    

@api_blueprint.route('/purchase_orders', methods=['POST'] )
def post_purchase_order():
    request_data = request.get_json()
    if type(request_data) != list:
        abort(400, description="Use an array to POST one or many purchase orders.")
    for po in request_data:
        new_order = PurchaseOrdersModel(description=po['description'])
        try:
            db.session.add(new_order)
            db.session.commit()        
        except Exception as e:
            db.session.rollback()
            abort(400, description=f"{e}")
    return jsonify(request_data)

@api_blueprint.route('/purchase_orders/<int:id>/items', methods=['GET'])
def get_purchase_orders_items(id):
    purchase_order_items = PurchaseOrdersItemsModel.query.filter_by(purchase_order_id=id).all()
    if purchase_order_items:
            return jsonify([po_item.to_dict() for po_item in purchase_order_items])
    abort(404, description=f"No items found for the purchase order of id {id}.")

@api_blueprint.route('/purchase_orders/<int:id>/items', methods=['POST'])
def put_order_items(id):
    request_data = request.get_json()
    if type(request_data) != list:
        abort(400, description="An order expects an array of item(s).")
    for po_item in request_data:
        new_order_item = PurchaseOrdersItemsModel(description=po_item['description'], price=po_item['price'], quantity=po_item['quantity'], purchase_order_id=id)
        try:
            db.session.add(new_order_item)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(404, description=f"No order found for id {id}.")
        except Exception as e:
            db.session.rollback()
            abort(400, description=f"{e}")        
    return jsonify(request_data)