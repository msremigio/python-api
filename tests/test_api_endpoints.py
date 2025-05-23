import json

def test_post_user(test_client):
    body = {'email': 'temp_test@email.com', 'password': 'temptestingapp'}

    response = test_client.post(
        'users',
        data=json.dumps(body),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.json['email'] == body['email']

def test_post_user_auth(test_client):
    body = {'email': 'perm_test_user@email.com', 'password': 'testingapp'}

    response = test_client.post(
        'users/authenticate',
        data=json.dumps(body),
        content_type='application/json'
    )

    assert response.status_code == 200

def test_get_homepage(test_client, test_access_token):
    response = test_client.get('/', headers={'Authorization': f'Bearer {test_access_token}'})

    assert response.status_code == 200
    assert response.json['message'] == 'Welcome to the ***purchase_orders*** API homepage!'

def test_get_purchase_orders(test_client, seed_test_db, test_access_token):
    response = test_client.get('/purchase_orders', headers={'Authorization': f'Bearer {test_access_token}'})

    assert response.status_code == 200
    assert response.json[0]['id'] == seed_test_db['po'].id
    assert response.json[0]['description'] == seed_test_db['po'].description
    assert response.json[0]['status'] == seed_test_db['po'].status.value

def test_get_purchase_orders_by_id(test_client, seed_test_db, test_access_token):
    response = test_client.get(f'/purchase_orders/{seed_test_db['po'].id}', headers={'Authorization': f'Bearer {test_access_token}'})

    assert response.status_code == 200
    assert response.json['id'] == seed_test_db['po'].id
    assert response.json['description'] == seed_test_db['po'].description
    assert response.json['status'] == seed_test_db['po'].status.value

def test_get_purchase_orders_by_id_not_found(test_client, test_access_token):
    id = 9999
    response = test_client.get(f'/purchase_orders/{id}', headers={'Authorization': f'Bearer {test_access_token}'})
    
    assert response.status_code == 404
    assert response.json['error'] == f'404 Not Found: No order found for id {id}.'

def test_post_purchase_orders(test_client, test_access_token):
    body = [{'description': 'Test purchase order 2'}, {'description': 'Test purchase order 3'}]

    response = test_client.post(
        'purchase_orders',
        headers={'Authorization': f'Bearer {test_access_token}'},
        data=json.dumps(body),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.json[0]['description'] == body[0]['description']
    assert response.json[1]['description'] == body[1]['description'] 

def test_post_purchase_orders_error(test_client, test_access_token):
    body = {'description': 'Purchase order 2'}

    response = test_client.post(
        'purchase_orders',
        headers={'Authorization': f'Bearer {test_access_token}'},
        data=json.dumps(body),
        content_type='application/json'
    )

    assert response.status_code == 400
    assert response.json['error'] == '400 Bad Request: Use an array to POST one or many purchase orders.'    

def test_get_purchase_orders_items_by_id(test_client, seed_test_db, test_access_token):
    response = test_client.get(f'/purchase_orders/{seed_test_db['po'].id}/items', headers={'Authorization': f'Bearer {test_access_token}'})

    assert response.status_code == 200
    assert response.json[0]['id'] == seed_test_db['poi'].id
    assert response.json[0]['description'] == seed_test_db['poi'].description
    assert response.json[0]['price'] == seed_test_db['poi'].price
    assert response.json[0]['quantity'] == seed_test_db['poi'].quantity

def test_get_purchase_orders_items_by_id_not_found(test_client, test_access_token):
    id = 9999
    response = test_client.get(f'/purchase_orders/{id}', headers={'Authorization': f'Bearer {test_access_token}'})
    
    assert response.status_code == 404
    assert response.json['error'] == f'404 Not Found: No order found for id {id}.'

def test_post_purchase_orders_items_by_id(test_client, seed_test_db, test_access_token): 
    body = [{'description': f'Second test item from purchase order {seed_test_db["po"].id}', 'price': 99.99, 'quantity': 3}, {'description': f'Third item from purchase order {seed_test_db["po"].id}', 'price': 49.90, 'quantity': 7}]

    response = test_client.post(
        f'purchase_orders/{seed_test_db["po"].id}/items',
        headers={'Authorization': f'Bearer {test_access_token}'},
        data=json.dumps(body),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.json[0]['description'] == body[0]['description']
    assert response.json[0]['price'] == body[0]['price']
    assert response.json[0]['quantity'] == body[0]['quantity']
    assert response.json[1]['description'] == body[1]['description']
    assert response.json[1]['price'] == body[1]['price']
    assert response.json[1]['quantity'] == body[1]['quantity']

def test_post_purchase_orders_items_by_id_not_found(test_client, test_access_token):
    id = 9999
    body = [{'description': f'First item from purchase order {id}', 'price': 99.99, 'quantity': 3}]

    response = test_client.post(
        f'purchase_orders/{id}/items',
        headers={'Authorization': f'Bearer {test_access_token}'},
        data=json.dumps(body),
        content_type='application/json'
    )

    assert response.status_code == 404
    assert response.json['error'] == f'404 Not Found: No order found for id {id}.'

def test_post_purchase_orders_items_by_id_error(test_client, test_access_token):
    body = {'description': 'Second item from purchase order 1', 'price': 99.99, 'quantity': 3}

    response = test_client.post(
        'purchase_orders/1/items',
        headers={'Authorization': f'Bearer {test_access_token}'},
        data=json.dumps(body),
        content_type='application/json'
    )

    assert response.status_code == 400
    assert response.json['error'] == '400 Bad Request: An order expects an array of item(s).'