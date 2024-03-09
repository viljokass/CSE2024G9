import os
import subprocess
import sys
import time
import unittest

import requests


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MAIN_PATH = os.path.join(PROJECT_ROOT, "main.py")
sys.path.insert(0, PROJECT_ROOT)

API_URL = "http://127.0.0.1:5000"
ORDERS_ENDPOINT = f"{API_URL}/v1/orders"  # Endpoint for posting an order
TRADES_ENDPOINT = f"{API_URL}/v1/trades"  # Endpoint for getting trades
M1 = 100
M2 = 200



class TestE2EScenario1(unittest.TestCase):
    """
    Verify input prices are validated based on latest market data
    a. Fetch current market last trade price of AAPL - example M1
    b. Verify Bid order at Price M1 x 1.08 is accepted
    c. Verify Offer order at Price M1 x 0.90 is accepted
    d. Verify Bid order at Price M1 x 1.11 is rejected
    e. Verify Offer order at Price M1 x -1.01 is rejected
    f. Verify no trades have happened
    """

    @classmethod
    def setUpClass(cls):
        # Start the app in a subprocess and with test database
        cls.api_server = subprocess.Popen(["python", MAIN_PATH, "--test"])

        #  Delay to ensure the server has started before running the tests
        time.sleep(2)

    def test_fetch_last_traded_price(self):
        response = requests.get(TRADES_ENDPOINT)
        assert response.status_code == 200
        assert response.json() == []

    def test_verify_bid_order_at_accepted_price(self):
        bid = {"type": "bid", "price": M1 * 1.08, "quantity": 100}
        response = requests.post(ORDERS_ENDPOINT, json=bid)
        assert response.status_code == 201

    def test_verify_offer_at_accepted_price(self):
        offer = {"type": "offer", "price": M1 * 0.90, "quantity": 100}
        response = requests.post(ORDERS_ENDPOINT, json=offer)
        assert response.status_code == 201

    def test_verify_bid_order_at_rejected_price(self):
        bid_2 = {"type": "bid", "price": M1 * 1.11, "quantity": 100}
        response = requests.post(ORDERS_ENDPOINT, json=bid_2)
        assert response.status_code == 406

    def test_verify_offer_order_at_rejected_price(self):
        offer_2 = {"type": "offer", "price": M1 * -1.01, "quantity": 100}
        response = requests.post(ORDERS_ENDPOINT, json=offer_2)
        assert response.status_code == 406

    def test_verify_no_trades_happened(self):
        response = requests.get(TRADES_ENDPOINT)
        assert response.status_code == 200
        assert response.json() == []

    def tearDown(self):
        self.api_server.kill()

# class TestE2EScenario2(unittest.TestCase):
#     """
#     Verify input quantity is valid
#     a. Fetch current market last trade price of AAPL - M2
#     b. Bid order at Price M2, Qty 0 is rejected
#     c. Bid order at Price M2, Qty 10.1 is rejected
#     d. Offer order at Price M2, Qty -100 is rejected
#     e. Verify no trades have happened
#     """
#
#     @classmethod
#     def setUpClass(cls):
#         # Start the app in a subprocess and with test database
#         cls.api_server = subprocess.Popen(["python", MAIN_PATH, "--test"])
#
#         #  Delay to ensure the server has started before running the tests
#         time.sleep(2)
#
#     def test_fetch_last_traded_price(self):
#         response = requests.get(TRADES_ENDPOINT)
#         assert response.status_code == 200
#         assert response.json() == []
#
#     def test_bid_order_at_zero_quantity(self):
#         bid = {"type": "bid", "price": M2, "quantity": 0}
#         response = requests.post(ORDERS_ENDPOINT, json=bid)
#         assert response.status_code == 406
#
#     def test_bid_order_at_float_quantity(self):
#         bid = {"type": "bid", "price": M2, "quantity": 10.1}
#         response = requests.post(ORDERS_ENDPOINT, json=bid)
#         assert response.status_code == 406
#
#     def test_offer_order_at_negative_quantity(self):
#         offer = {"type": "offer", "price": M2, "quantity": -100}
#         response = requests.post(ORDERS_ENDPOINT, json=offer)
#         assert response.status_code == 406
#
#     def test_verify_no_trades_happened(self):
#         response = requests.get(TRADES_ENDPOINT)
#         assert response.status_code == 200
#         assert response.json() == []
#
#     def tearDown(self):
#         self.api_server.kill()