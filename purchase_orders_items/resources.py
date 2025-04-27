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


class PurchaseOrdersItems(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'id',
        type=int,
        required=True,
        help="Must inform an item id(int)."
    )
    parser.add_argument(
        'description',
        type=str,
        required=True,
        help="Must inform an item description(str)."
    )
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="Must inform an item price(float)."
    )
    parser.add_argument(
        'quantity',
        type=int,
        required=True,
        help="Must inform a quantity for an item(int)."
    )

    def get(self, id):
        for order in purchase_orders:
            if id == order['id']:
                return jsonify(order['items'])
        return jsonify({'message': f'No order found for id {id}.'})
    
    def put(self,id):
        request_data = PurchaseOrdersItems.parser.parse_args()
        for order in purchase_orders:
            if id == order['id']:
                order['items'].append(request_data)
                return jsonify(order)

        return jsonify({'message': f'No order found for id {id}.'})