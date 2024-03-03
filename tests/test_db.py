import os
import sys
import unittest
import json

from dotenv import dotenv_values

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from models.order import Order
from models.trade import Trade
from db_handler import DbHandler


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUp(cls):
        # Change to the test database from the environment variables
        os.environ['db'] = dotenv_values("../.env", ).get('TEST_DB_NAME')
        cls.test_db = DbHandler()

    def test_record_trade(self):
        # Assert that the trade is successfully recorded and retrieved
        trade = Trade(100, 100.00)
        response = self.test_db.record_trade(trade)
        self.assertEqual(response.acknowledged, True)
        trade_id = response.inserted_id
        trades_json = self.test_db.get_trades()
        trades_list = json.loads(trades_json)
        self.assertEqual(trades_list[0]['quantity'], trade.quantity, "Should be 100")
        self.assertEqual(trades_list[0]['price'], trade.price, "Should be 100.00")
        self.assertEqual(trades_list[0]['_id']['$oid'], str(trade_id), "Should be the same")
        self.assertEqual(len(trades_list), 1, "Should be 1")

    def test_record_order(self):
        # Assert that the order is successfully recorded and retrieved
        order = Order('bid', 100, 100.00)
        response = self.test_db.record_order(order)
        self.assertEqual(response.acknowledged, True)
        order_id = response.inserted_id
        orders_json = self.test_db.get_orders()
        orders_list = json.loads(orders_json)
        self.assertEqual(orders_list[0]['type'], order.type, "Should be bid")
        self.assertEqual(orders_list[0]['quantity'], order.quantity, "Should be 100")
        self.assertEqual(orders_list[0]['price'], order.price, "Should be 100.00")
        self.assertEqual(orders_list[0]['_id']['$oid'], str(order_id), "Should be the same")

    def test_delete_trade(self):
        # Assert that a trade is successfully deleted
        trade = Trade(100, 100.00)
        response = self.test_db.record_trade(trade)
        trade_id = response.inserted_id
        response = self.test_db.delete_trade(trade_id)
        self.assertEqual(response.acknowledged, True)
        self.assertEqual(response.deleted_count, 1)
        self.assertEqual(self.test_db.get_trades(), "[]")

    def test_delete_order(self):
        # Assert that an order is successfully deleted
        order = Order('bid', 100, 100.00)
        response = self.test_db.record_order(order)
        order_id = response.inserted_id
        response = self.test_db.delete_order(order_id)
        self.assertEqual(response.acknowledged, True)
        self.assertEqual(response.deleted_count, 1)
        self.assertEqual(self.test_db.get_orders(), "[]")

    def tearDown(self):
        # Delete all trades and orders from the test database after each test
        self.test_db.delete_trades()
        self.test_db.delete_orders()
        # Change back to the main database from the environment variables
        os.environ['db'] = dotenv_values("../.env", ).get('DB_NAME')
