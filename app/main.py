from dotenv import load_dotenv
from flask import Flask, jsonify, request, abort

load_dotenv()

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

def create_app():
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def home():
        return "Welcome to the ***purchase_orders*** API homepage!"
    
    @app.route('/purchase_orders', methods=['GET'])
    def get_purchase_orders():
        return jsonify(purchase_orders)    

    return app