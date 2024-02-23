import pytest
import os
import sys

# Get the tested module path
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root)

from routes import create_app

# Get the test app
@pytest.fixture()
def app():
    app = create_app()
    app.config['TESTING'] == True
    return app

# Get the client
@pytest.fixture()
def client(app):
    return app.test_client()

# Testing get for trade and order endpoints.
def test_get(client):
    
    # Test that trade get is OK
    response = client.get("/v1/trades")
    assert response.status_code == 200
    
    # Test that order get is not implemented
    response = client.get("/v1/orders")
    assert response.status_code == 405

# Testing post for trade and order endpoints.
def test_post(client):
    
    # Test that trades refuse posts (unimplemented methods)
    response = client.post("/v1/trades")
    assert response.status_code == 405

    # Test that orders approve json posts and validates the data
    ## Data OK (Offer)
    response = client.post("/v1/orders", json = {
        "order_type": "Offer",
        "unit_price": 199.99,
        "quantity" : 69
    })
    assert response.status_code == 201

    # Data OK (Bid)
    response = client.post("/v1/orders", json = {
        "order_type": "Bid",
        "unit_price": 199.99,
        "quantity" : 69
    })
    assert response.status_code == 201

    ## Data not OK, a fault in field names
    response = client.post("/v1/orders", json = {
        "order_typpe": "Offer",
        "unit_pricce": 189.33,
        "quntity": 29
    })
    assert response.status_code == 400

    ## Data not OK, a fault in data
    response = client.post("/v1/orders", json = {
        "order_type": "Bobr",
        "unit_price": "a2233",
        "quantity": "k",
    })
    assert response.status_code == 400
