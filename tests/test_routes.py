import pytest
import os
import sys

# Get the tested module path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from routes import create_app
import mongomock
from db_handler import DbHandler
from models.trade import Trade

# Mock database handler that we'll attach to the Flask App
mock_client = mongomock.MongoClient("testdb")["testdb"]
db_handler = DbHandler(mock_client)


# Get the test app
@pytest.fixture()
def app():
    app = create_app(db_handler)
    app.config["TESTING"] = True
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

    # Test that there's data and that it's correct
    trade = Trade(5, 190.24)
    db_handler.record_trade(trade=trade)
    response = client.get("/v1/trades")
    assert response.status_code == 200
    assert b'"quantity"' and b"5" in response.data
    assert b'"price"' and b"190.24" in response.data

    # Test that order get is not implemented
    response = client.get("/v1/orders")
    assert response.status_code == 405


# Testing post for trade and order endpoints.
def test_post(client):

    # Test that trades refuse posts (unimplemented methods)
    response = client.post("/v1/trades")
    assert response.status_code == 405

    # Test that orders approve json posts and validates the data
    db_handler.record_last_traded_price(100.0)

    # Data OK (Offer, not compliant to the 10%)
    response = client.post(
        "/v1/orders", json={"type": "offer", "price": 199.99, "quantity": 69}
    )
    assert response.status_code == 406

    # Data OK (Bid, not compliant to the 10%)
    response = client.post(
        "/v1/orders", json={"type": "bid", "price": 199.99, "quantity": 69}
    )
    assert response.status_code == 406

    # Test that orders approve json posts and validates the data
    db_handler.record_last_traded_price(300.0)

    # Data OK (Offer, not compliant to the 10%)
    response = client.post(
        "/v1/orders", json={"type": "offer", "price": 199.99, "quantity": 69}
    )
    assert response.status_code == 406

    # Data OK (Bid, not compliant to the 10%)
    response = client.post(
        "/v1/orders", json={"type": "bid", "price": 199.99, "quantity": 69}
    )
    assert response.status_code == 406

    db_handler.record_last_traded_price(200.0)

    # Data OK (Offer, compliant to the 10%)
    response = client.post(
        "/v1/orders", json={"type": "offer", "price": 180.00, "quantity": 69}
    )
    assert response.status_code == 201
    assert '"type": "offer"' in db_handler.get_orders()

    db_handler.delete_orders()

    # Data OK (Bid, compliant to the 10%)
    response = client.post(
        "/v1/orders", json={"type": "bid", "price": 180.00, "quantity": 69}
    )
    assert response.status_code == 201
    assert '"type": "bid"' in db_handler.get_orders()

    # Data not OK, a fault in field names
    response = client.post(
        "/v1/orders", json={"typpe": "Offer", "pricce": 189.33, "quntity": 29}
    )
    assert response.status_code == 400

    # Data not OK, a fault in data
    response = client.post(
        "/v1/orders",
        json={
            "type": "Bobr",
            "price": "a2233",
            "quantity": "k",
        },
    )

    # Data not OK, a fault in data
    response = client.post(
        "/v1/orders",
        json={
            "type": "Bobr",
            "price": 139.23,
            "quantity": 23,
        },
    )
    assert response.status_code == 400

    ## Data not OK, a fault in data
    response = client.post("/v1/orders", json = {
        "type": "Bobr",
        "price": "a2233",
        "quantity": "k",
    })

    ## Data not OK, a fault in data
    response = client.post("/v1/orders", json = {
        "type": "Bobr",
        "price": 139.23,
        "quantity": 23,
    })
    assert response.status_code == 400

# Like in the examples in the Project Details
def test_order_matching(client):

    db_handler.delete_orders()
    db_handler.delete_trades()
    db_handler.record_last_traded_price(190.0)

    client.post("/v1/orders", json = {
        "type": "bid",
        "price": 200.0,
        "quantity" : 1000
    })

    db_handler.record_last_traded_price(200.0)

    client.post("/v1/orders", json = {
        "type": "bid",
        "price": 210.0,
        "quantity" : 500
    })

    response = client.post("/v1/orders", json = {
        "type": "offer",
        "price": 225.0,
        "quantity" : 750
    })

    assert response.status_code == 406

    client.post("/v1/orders", json = {
        "type": "offer",
        "price": 205.0,
        "quantity" : 500
    })

    response = client.get("/v1/trades")
    assert response.status_code == 200
    assert b"\"quantity\": 500, \"price\": 210.0" in response.data

    client.post("/v1/orders", json = {
        "type": "offer",
        "price": 200.0,
        "quantity" : 1500
    })

    response = client.get("/v1/trades")
    assert response.status_code == 200
    assert b"\"quantity\": 500, \"price\": 210.0" in response.data
    assert b"\"quantity\": 1000, \"price\": 200.0" in response.data

    client.post("/v1/orders", json = {
        "type": "offer",
        "price": 200.0,
        "quantity" : 750
    })

    client.post("/v1/orders", json = {
        "type": "bid",
        "price": 200.0,
        "quantity" : 1000
    })

    response = client.get("/v1/trades")
    assert response.status_code == 200
    assert b"\"quantity\": 500, \"price\": 210.0, \"time\": " in response.data
    assert b"\"quantity\": 1000, \"price\": 200.0, \"time\": " in response.data
    assert b"\"quantity\": 500, \"price\": 200.0, \"time\": " in response.data

