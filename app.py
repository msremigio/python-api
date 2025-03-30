from flask import Flask, jsonify, request

app = Flask(__name__)

purchase_orders = [
    {
        'id': 1,
        'description': 'Purchase order 1',
        'items': [
            {
                'id': 1,
                'description': 'First item from purchase order 1',
                'price': 20.99
            }
        ]
    }
]


@app.route('/', methods=['GET'])
def home():
    return "Hello World!"

@app.route('/purchase_orders', methods=['GET'])
def get_purchase_orders():
    return jsonify(purchase_orders)

@app.route('/purchase_orders/<int:id>', methods=['GET'])
def get_purchase_orders_by_id(id):
    for order in purchase_orders:
        if id == order['id']:
            return jsonify(order)
    return jsonify({'message': f'No order found for id {id}.'})

@app.route('/purchase_orders', methods=['POST'] )
def create_purchase_order():
    request_data = request.get_json()
    order = {
        'id': request_data['id'],
        'description': request_data['description'],
        'items': []
    }

    purchase_orders.append(order)
    
    return jsonify(order)




app.run(port=5000)