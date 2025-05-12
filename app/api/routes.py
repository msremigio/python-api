from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.services.users_service import UsersService
from app.services.purchase_orders_service import PurchaseOrdersService
from app.services.purchase_orders_items_service import PurchaseOrdersItemsService


api_blueprint = Blueprint('api', __name__)


@api_blueprint.errorhandler(400)
def bad_request(e):
     return jsonify(error = str(e)), 400

@api_blueprint.errorhandler(401)
def unathorized(e):
     return jsonify(error = str(e)), 401

@api_blueprint.errorhandler(404)
def not_found(e):
     return jsonify(error = str(e)), 404

@api_blueprint.errorhandler(500)
def internal_server_error(e):
     return jsonify(error = str(e)), 500

@api_blueprint.route('/users', methods=['POST'])
def post_user():
    request_data = request.get_json()
    return UsersService.post_user(request_data)

@api_blueprint.route('/users/authenticate', methods=['POST'])
def user_auth():
    request_data = request.get_json()
    return UsersService.authenticate(request_data)

@api_blueprint.route('/', methods=['GET'])
@jwt_required()
def home():
    return jsonify({'message': 'Welcome to the ***purchase_orders*** API homepage!'})

@api_blueprint.route('/purchase_orders', methods=['GET'])
@jwt_required()
def get_purchase_orders():  
    return PurchaseOrdersService.get_all()

@api_blueprint.route('/purchase_orders/<int:id>', methods=['GET'])
@jwt_required()
def get_purchase_orders_by_id(id):
    return PurchaseOrdersService.get_by_id(id)  

@api_blueprint.route('/purchase_orders', methods=['POST'])
@jwt_required()
def post_purchase_order():
    request_data = request.get_json()
    return PurchaseOrdersService.post_all(request_data)

@api_blueprint.route('/purchase_orders/<int:id>/items', methods=['GET'])
@jwt_required()
def get_purchase_orders_items(id):
    return PurchaseOrdersItemsService.get_all_by_id(id)

@api_blueprint.route('/purchase_orders/<int:id>/items', methods=['POST'])
@jwt_required()
def post_order_items(id):
    request_data = request.get_json()
    return PurchaseOrdersItemsService.post_all_by_id(id, request_data)