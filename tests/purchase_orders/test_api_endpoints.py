import json

def test_get_homepage(test_client):
    response = test_client.get('/')

    assert response.status_code == 200
    assert response.json['message'] == 'Welcome to the ***purchase_orders*** API homepage!'

def test_get_purchase_orders(test_client):
    response = test_client.get('/purchase_orders')

    assert response.status_code == 200
    assert response.json[0]['id'] == 1
    assert response.json[0]['description'] == 'Purchase order 1'

def test_get_purchase_orders_by_id(test_client):
    response = test_client.get('/purchase_orders/1')

    assert response.status_code == 200
    assert response.json['id'] == 1
    assert response.json['description'] == 'Purchase order 1'

def test_get_purchase_orders_by_id_not_found(test_client):
    response = test_client.get('/purchase_orders/999')
    
    assert response.json['message'] == 'No order found for id 999.'

def test_post_purchase_orders(test_client):
    body = [{'id': 2, 'description': 'Purchase order 2'}, {'id': 3, 'description': 'Purchase order 3'}]

    response = test_client.post(
        'purchase_orders',
        data=json.dumps(body),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.json[0]['id'] == body[0]['id']
    assert response.json[0]['description'] == body[0]['description']
    assert response.json[1]['id'] == body[1]['id']
    assert response.json[1]['description'] == body[1]['description'] 

def test_post_purchase_orders_error(test_client):
    body = {'id': 2, 'description': 'Purchase order 2'}

    response = test_client.post(
        'purchase_orders',
        data=json.dumps(body),
        content_type='application/json'
    )

    assert response.status_code == 400
    assert response.json['error'] == '400 Bad Request: Use an array to POST one or many purchase orders.'    

def test_get_purchase_orders_items_by_id(test_client):
    response = test_client.get('/purchase_orders/1/items')

    assert response.status_code == 200
    assert response.json[0]['id'] == 1
    assert response.json[0]['description'] == 'First item from purchase order 1'
    assert response.json[0]['price'] == 20.99
    assert response.json[0]['quantity'] == 2

def test_get_purchase_orders_items_by_id_not_found(test_client):
    response = test_client.get('/purchase_orders/999/items')

    assert response.json['message'] == 'No order found for id 999.'

def test_put_purchase_orders_items_by_id(test_client): 
    body = [{'id': 2, 'description': 'Second item from purchase order 1', 'price': 99.99, 'quantity': 3}, {'id': 3, 'description': 'Third item from purchase order 1', 'price': 49.90, 'quantity': 7}]

    response = test_client.put(
        'purchase_orders/1/items',
        data=json.dumps(body),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.json['items'][1]['id'] == body[0]['id']
    assert response.json['items'][1]['description'] == body[0]['description']
    assert response.json['items'][1]['price'] == body[0]['price']
    assert response.json['items'][1]['quantity'] == body[0]['quantity']
    assert response.json['items'][2]['id'] == body[1]['id']
    assert response.json['items'][2]['description'] == body[1]['description'] 
    assert response.json['items'][2]['price'] == body[1]['price']
    assert response.json['items'][2]['quantity'] == body[1]['quantity']

def test_put_purchase_orders_items_by_id_not_found(test_client):
    body = [{'id': 1, 'description': 'First item from purchase order 999', 'price': 99.99, 'quantity': 3}]

    response = test_client.put(
        'purchase_orders/999/items',
        data=json.dumps(body),
        content_type='application/json'
    )

    assert response.json['message'] == 'No order found for id 999.' 

def test_put_purchase_orders_items_by_id_error(test_client):
    body = {'id': 2, 'description': 'Second item from purchase order 1', 'price': 99.99, 'quantity': 3}

    response = test_client.put(
        'purchase_orders/1/items',
        data=json.dumps(body),
        content_type='application/json'
    )

    assert response.status_code == 400
    assert response.json['error'] == '400 Bad Request: An order expects an array of item(s).'