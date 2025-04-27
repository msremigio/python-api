from flask import jsonify
from flask_restful import Resource, reqparse

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

class PurchaseOrders(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'id',
        type=int,
        required=True,
        help="Must inform an order id(int)."
    )
    parser.add_argument(
        'description',
        type=str,
        required=True,
        help="Must inform an order description(str)."
    )

    def get(self):
        return jsonify(purchase_orders)
    
    def post(self):
        request_data = PurchaseOrders().parser.parse_args()
        order = {
        'id': request_data['id'],
        'description': request_data['description'],
        'items': []
        }

        purchase_orders.append(order)
    
        return jsonify(order)
    
class PurchaseOrdersById(Resource):
    def get(self, id):
        for order in purchase_orders:
            if id == order['id']:
                return jsonify(order)
        return jsonify({'message': f'No order found for id {id}.'})
