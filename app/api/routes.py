from flask import Blueprint, jsonify, request, abort

api_blueprint = Blueprint('api', __name__)

purchase_orders = [
    {
        'id': 1,
        'description': 'Purchase order 1',
        'items': [
            {
                'id': 1,
                'description': 'First item from purchase order 1',
                'price': 20.99,
                'quantity': 2
            }
        ]
    }
]

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
    return jsonify(purchase_orders)    

@api_blueprint.route('/purchase_orders/<int:id>', methods=['GET'])
def get_purchase_orders_by_id(id):
    for order in purchase_orders:
        if id == order['id']:
            return jsonify(order)
    abort(404, description=f"No order found for id {id}.")

@api_blueprint.route('/purchase_orders', methods=['POST'] )
def post_purchase_order():
    request_data = request.get_json()
    if type(request_data) != list:
        abort(400, description="Use an array to POST one or many purchase orders.")
    for po in request_data:
        order = {
            'id': po['id'],
            'description': po['description'],
            'items': []
        }
        purchase_orders.append(order)
    
    return jsonify(request_data)

@api_blueprint.route('/purchase_orders/<int:id>/items', methods=['GET'])
def get_purchase_orders_items(id):
    for order in purchase_orders:
        if id == order['id']:
            return jsonify(order['items'])
    abort(404, description=f"No order found for id {id}.")

@api_blueprint.route('/purchase_orders/<int:id>/items', methods=['PUT'])
def put_order_items(id):
    request_data = request.get_json()
    if type(request_data) != list:
        abort(400, description="An order expects an array of item(s).")
    for order in purchase_orders:
        if id == order['id']:
            _ = [order['items'].append(order_item) for order_item in request_data]
            return jsonify(order)

    abort(404, description=f"No order found for id {id}.")