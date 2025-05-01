def test_get_homepage(test_client):
    response = test_client.get('/')

    assert response.status_code == 200
    assert response.text == 'Welcome to the ***purchase_orders*** API homepage!'

def test_get_purchase_orders(test_client):
    response = test_client.get('/purchase_orders')

    assert response.status_code == 200
    assert response.json[0]['id'] == 1
    assert response.json[0]['description'] == 'Purchase order 1'